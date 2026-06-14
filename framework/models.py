from dataclasses import dataclass


@dataclass(frozen=True)
class TestCase:
    sheet: str
    row_number: int
    test_case_id: str
    category: str
    region: str
    role: str
    prompt: str
    expected_behavior: str
    must_not_do: str
    pass_criteria: str
    risk: str
    testing_layer: str

    @property
    def is_api(self) -> bool:
        return self.testing_layer.lower() in {"api", "both"}

    @property
    def is_ui(self) -> bool:
        return self.testing_layer.lower() in {"ui", "both"}

    @property
    def is_spec_gap(self) -> bool:
        text = f"{self.category} {self.expected_behavior} {self.pass_criteria}".lower()
        return "spec gap" in text or "document actual behavior" in text

