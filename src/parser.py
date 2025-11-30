import ast
import logging

class MethodVisitor(ast.NodeVisitor):
    def __init__(self):
        self.steps = []
        self.variables = {} # Map variable name to element info

    def visit_Assign(self, node):
        # Handle: var = driver.find_element(...)
        if isinstance(node.value, ast.Call):
            self._handle_call(node.value, assigned_to=node.targets[0])
        self.generic_visit(node)

    def visit_Expr(self, node):
        # Handle: element.click() or driver.get(...)
        if isinstance(node.value, ast.Call):
            self._handle_call(node.value)
        else:
            self.steps.append({"action": "unknown", "details": "Non-call expression"})
        self.generic_visit(node)

    def _handle_call(self, call_node, assigned_to=None):
        func = call_node.func
        
        # Handle built-in functions like print()
        if isinstance(func, ast.Name):
            if func.id == "print":
                if call_node.args:
                    arg = call_node.args[0]
                    text = arg.value if isinstance(arg, ast.Constant) else "UNKNOWN_TEXT"
                    self.steps.append({"action": "print", "text": text})
                return

        if isinstance(func, ast.Attribute):
            # obj.method()
            obj_name = self._get_name(func.value)
            method_name = func.attr
            
            if method_name == "get":
                # driver.get("url")
                if call_node.args:
                    arg = call_node.args[0]
                    url = arg.value if isinstance(arg, ast.Constant) else "UNKNOWN_URL"
                    self.steps.append({"action": "navigate", "url": url})
            
            elif method_name == "sleep" and obj_name == "time":
                # time.sleep(seconds)
                if call_node.args:
                    arg = call_node.args[0]
                    seconds = arg.value if isinstance(arg, ast.Constant) else 0
                    self.steps.append({"action": "sleep", "seconds": seconds})

            elif method_name == "find_element":
                # driver.find_element(By.ID, "foo")
                strategy, value = self._extract_find_args(call_node.args)
                if assigned_to and isinstance(assigned_to, ast.Name):
                    self.variables[assigned_to.id] = {"strategy": strategy, "value": value}
            
            elif method_name == "click":
                # element.click()
                selector = None
                if obj_name in self.variables:
                    selector = self.variables[obj_name]
                elif isinstance(func.value, ast.Call):
                    # Handle chained: driver.find_element(...).click()
                    inner_call = func.value
                    if isinstance(inner_call.func, ast.Attribute) and inner_call.func.attr == "find_element":
                        strategy, value = self._extract_find_args(inner_call.args)
                        selector = {"strategy": strategy, "value": value}

                if selector:
                    self.steps.append({"action": "click", "selector": selector})
                else:
                    self.steps.append({"action": "unknown", "details": f"Click on unknown object: {obj_name}"})
            
            elif method_name == "send_keys":
                # element.send_keys("text")
                selector = None
                if obj_name in self.variables:
                    selector = self.variables[obj_name]
                elif isinstance(func.value, ast.Call):
                     # Handle chained: driver.find_element(...).send_keys(...)
                    inner_call = func.value
                    if isinstance(inner_call.func, ast.Attribute) and inner_call.func.attr == "find_element":
                        strategy, value = self._extract_find_args(inner_call.args)
                        selector = {"strategy": strategy, "value": value}

                if selector and call_node.args:
                    arg = call_node.args[0]
                    text = arg.value if isinstance(arg, ast.Constant) else "UNKNOWN_TEXT"
                    self.steps.append({"action": "input", "selector": selector, "text": text})
                else:
                    self.steps.append({"action": "unknown", "details": f"Send keys to unknown object: {obj_name}"})
            
            elif method_name == "back":
                # driver.back()
                self.steps.append({"action": "back"})

            elif method_name == "clear":
                # element.clear()
                if obj_name in self.variables:
                    element = self.variables[obj_name]
                    self.steps.append({"action": "clear", "selector": element})
                else:
                    self.steps.append({"action": "unknown", "details": f"Clear unknown object: {obj_name}"})

            elif method_name == "swipe":
                # driver.swipe(start_x, start_y, end_x, end_y, duration)
                # Simplified capture, assuming args are present
                self.steps.append({"action": "swipe", "args": [a.value if isinstance(a, ast.Constant) else 0 for a in call_node.args]})

            elif method_name in ["Chrome", "Firefox", "Edge", "Safari", "Remote"]:
                # Ignore driver initialization
                pass

            else:
                self.steps.append({"action": "unknown", "details": f"Unknown method call: {method_name}"})
        else:
             self.steps.append({"action": "unknown", "details": "Unknown function call"})

    def visit_Assert(self, node):
        # Handle: assert "text" in element.text
        # This is a bit complex to parse fully, but we can try to capture simple inclusion checks
        if isinstance(node.test, ast.Compare):
            # "text" in element.text
            if isinstance(node.test.ops[0], ast.In):
                left = node.test.left
                if isinstance(left, ast.Constant):
                    text = left.value
                    self.steps.append({"action": "assert_visible", "text": text})
                    return
        
        self.steps.append({"action": "unknown", "details": "Unsupported assertion"})

    def visit_If(self, node):
        self.steps.append({"action": "unknown", "details": "Unsupported control flow: If statement"})
        # We stop traversal here to avoid flattening the body
    
    def visit_For(self, node):
        self.steps.append({"action": "unknown", "details": "Unsupported control flow: For loop"})
    
    def visit_While(self, node):
        self.steps.append({"action": "unknown", "details": "Unsupported control flow: While loop"})

    def _get_name(self, node):
        if isinstance(node, ast.Name):
            return node.id
        return None

    def _extract_find_args(self, args):
        # Expecting (By.ID, "value") or ("id", "value")
        if len(args) < 2:
            return None, None
        
        # Strategy
        strategy_arg = args[0]
        strategy = "unknown"
        if isinstance(strategy_arg, ast.Attribute): # By.ID
            strategy = strategy_arg.attr
        elif isinstance(strategy_arg, ast.Constant):
            strategy = strategy_arg.value
            
        # Value
        value_arg = args[1]
        value = value_arg.value if isinstance(value_arg, ast.Constant) else "UNKNOWN_SELECTOR"
        
        return strategy, value


class TestVisitor(ast.NodeVisitor):
    def __init__(self):
        self.tests = []

    def visit_FunctionDef(self, node):
        if node.name.startswith("test_"):
            visitor = MethodVisitor()
            visitor.visit(node)
            self.tests.append({
                "name": node.name,
                "steps": visitor.steps
            })
        self.generic_visit(node)

class PythonParser:
    def parse(self, file_path):
        """
        Parses a Python file and extracts relevant automation steps.
        Returns a list of test definitions.
        """
        logging.info(f"Parsing {file_path}")
        with open(file_path, "r") as f:
            tree = ast.parse(f.read())
        
        visitor = TestVisitor()
        visitor.visit(tree)
        return visitor.tests
