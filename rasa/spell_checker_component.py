from typing import Any, Text, Dict, List
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from spellchecker import SpellChecker

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER, is_trainable=False
)
class SpellCheckerComponent(GraphComponent):
    @staticmethod
    def required_components() -> List:
        return []

    def __init__(self, config: Dict[Text, Any]) -> None:
        self.spell = SpellChecker()

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config)

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get("text")
            if text:
                corrected_text = self.correct_spelling(text)
                message.set("text", corrected_text)
        return messages

    def correct_spelling(self, text: Text) -> Text:
        words = text.split()
        corrected_words = [
            self.spell.correction(word) if word.isalpha() else word
            for word in words
        ]
        return " ".join(corrected_words)

    def train(self, training_data: TrainingData) -> GraphComponent:
        return self

    # ✅ Add this method to fix the error during rasa train
    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        # Optionally, correct spelling in training examples here
        for example in training_data.training_examples:
            text = example.get("text")
            if text:
                corrected_text = self.correct_spelling(text)
                example.set("text", corrected_text)
        return training_data
