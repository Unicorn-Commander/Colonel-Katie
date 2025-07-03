import json
import os
from interpreter.core.workflow_manager import Workflow, SequentialStep, ParallelStep, ConditionalStep, HumanInLoopStep

class WorkflowTemplateManager:
    def __init__(self, template_dir="./workflow_templates"):
        self.template_dir = template_dir
        os.makedirs(self.template_dir, exist_ok=True)

    def save_workflow_template(self, workflow, filename=None):
        if filename is None:
            filename = f"{workflow.name.replace(' ', '_').lower()}.json"
        file_path = os.path.join(self.template_dir, filename)

        # Simple serialization for now. Will need more robust handling for complex step objects.
        workflow_data = {
            "name": workflow.name,
            "description": workflow.description,
            "steps": []
        }
        for step in workflow.steps:
            step_data = {"type": step.__class__.__name__}
            if isinstance(step, SequentialStep):
                step_data["agent_name"] = step.agent_name
                step_data["input_mapping"] = step.input_mapping
                step_data["output_mapping"] = step.output_mapping
            elif isinstance(step, ParallelStep):
                step_data["agent_names"] = step.agent_names
                step_data["input_mapping"] = step.input_mapping
                step_data["output_mapping"] = step.output_mapping
            elif isinstance(step, ConditionalStep):
                step_data["condition_agent_name"] = step.condition_agent_name
                step_data["condition_mapping"] = step.condition_mapping
                step_data["default_next_step"] = step.default_next_step
            elif isinstance(step, HumanInLoopStep):
                step_data["prompt_message"] = step.prompt_message
                step_data["expected_input_type"] = step.expected_input_type
            workflow_data["steps"].append(step_data)

        with open(file_path, "w") as f:
            json.dump(workflow_data, f, indent=4)
        print(f"Workflow template saved to {file_path}")

    def load_workflow_template(self, filename):
        file_path = os.path.join(self.template_dir, filename)
        if not os.path.exists(file_path):
            print(f"Error: Template file {file_path} not found.")
            return None

        with open(file_path, "r") as f:
            workflow_data = json.load(f)

        # Simple deserialization. Will need more robust handling.
        workflow = Workflow(workflow_data["name"], workflow_data.get("description", ""))
        for step_data in workflow_data["steps"]:
            step_type = step_data["type"]
            if step_type == "SequentialStep":
                step = SequentialStep(step_data["agent_name"], step_data["input_mapping"], step_data["output_mapping"])
            elif step_type == "ParallelStep":
                step = ParallelStep(step_data["agent_names"], step_data["input_mapping"], step_data["output_mapping"])
            elif step_type == "ConditionalStep":
                step = ConditionalStep(step_data["condition_agent_name"], step_data["condition_mapping"], step_data["default_next_step"])
            elif step_type == "HumanInLoopStep":
                step = HumanInLoopStep(step_data["prompt_message"], step_data["expected_input_type"])
            else:
                print(f"Warning: Unknown step type {step_type} during loading.")
                continue
            workflow.add_step(step)
        print(f"Workflow template loaded from {file_path}")
        return workflow

    def list_templates(self):
        return [f for f in os.listdir(self.template_dir) if f.endswith(".json")]
