class MaestroMapper:
    def map(self, tests):
        """
        Maps Python AST nodes/steps to Maestro commands.
        Returns a list of flows (one per test).
        """
        flows = []
        for test in tests:
            flow = {
                "appId": "com.example.app", # TODO: Make configurable
                "name": test["name"],
                "---": [
                    {"launchApp": {"clearState": True}}
                ]
            }
            
            commands = []
            has_errors = False
            for step in test["steps"]:
                cmd = self._map_step(step)
                if cmd:
                    if isinstance(cmd, list):
                        commands.extend(cmd)
                    else:
                        commands.append(cmd)
                        if "TODO_UNSUPPORTED_ACTION" in cmd:
                            has_errors = True
            
            flow["---"].extend(commands)
            if has_errors:
                flow["_has_errors"] = True
            flows.append(flow)
        
        return flows

    def _map_step(self, step):
        action = step.get("action")
        
        if action == "navigate":
            return {"openLink": step["url"]}
        
        elif action == "click":
            selector = self._map_selector(step["selector"])
            return {"tapOn": selector}
        
        elif action == "input":
            selector = self._map_selector(step["selector"])
            text = step["text"]
            # Maestro input: tap then type
            return [
                {"tapOn": selector},
                {"inputText": text}
            ]
            
        elif action == "print":
            # Map print to runScript console.log
            return {"runScript": f"console.log('{step['text']}')"}
            
        elif action == "sleep":
            # Map sleep to runScript delay
            ms = int(step["seconds"] * 1000)
            return {"runScript": f"await new Promise(resolve => setTimeout(resolve, {ms}))"}

        elif action == "back":
            return {"back": None}
            
        elif action == "clear":
            selector = self._map_selector(step["selector"])
            # Maestro eraseText works on focused element, so tap first
            return [
                {"tapOn": selector},
                {"eraseText": None}
            ]
            
        elif action == "swipe":
            # Simplified swipe mapping
            args = step.get("args", [])
            if len(args) >= 4:
                return {"swipe": {"start": f"{args[0]},{args[1]}", "end": f"{args[2]},{args[3]}"}}
            return {"TODO_UNSUPPORTED_ACTION": "Swipe requires start/end coordinates"}

        elif action == "assert_visible":
            return {"assertVisible": {"text": step["text"]}}

        elif action == "unknown":
            import logging
            details = step['details']
            logging.warning(f"Unknown step: {details}")
            
            suggestion = ""
            if "control flow" in details:
                suggestion = " (Suggestion: Unroll loops or use runScript for simple logic)"
            elif "Unknown method" in details:
                suggestion = " (Suggestion: Check if this can be mapped to a runScript or custom Maestro command)"
            
            return {"TODO_UNSUPPORTED_ACTION": f"{details}{suggestion}"}
            
        return None

    def _map_selector(self, selector_info):
        strategy = selector_info["strategy"]
        value = selector_info["value"]
        
        if strategy == "ID":
            return {"id": value}
        elif strategy == "TEXT":
            return {"text": value}
        elif strategy == "XPATH":
            # XPath not directly supported, fallback to text or warning
            return {"text": f"TODO_XPATH: {value}"} # Placeholder
        else:
            # Fallback
            return {"text": value}
