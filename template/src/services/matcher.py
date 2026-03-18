import torch
import open_clip
from core.config import settings
from schemas.match import MatchRequest, MatchResult

class MatcherService:
    _instance = None
    _model = None
    _preprocess = None
    _tokenizer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MatcherService, cls).__new__(cls)
            cls._instance._initialize_model()
        return cls._instance

    def _initialize_model(self):
        print(f"Loading model {settings.MODEL_NAME} with dataset {settings.DATASET_NAME}...")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        try:
            self._model, _, self._preprocess = open_clip.create_model_and_transforms(
                settings.MODEL_NAME,
                pretrained=settings.DATASET_NAME,
                cache_dir=settings.MODEL_CACHE_DIR
            )
            self._model.to(self.device)
            self._model.eval()
            self._tokenizer = open_clip.get_tokenizer(settings.MODEL_NAME)
            print("Model loaded successfully.")
        except Exception as e:
            print(f"Warning: Could not load model initially: {e}")

    async def find_matches(self, request: MatchRequest) -> list[MatchResult]:
        """
        Implementation logic inspired by f4-its (Fine-grained Feature Fusion).
        This fuses image embeddings with VLM-generated descriptions.
        """

        # Step 1: Preprocess the incoming image (if provided)
        # Step 2: Tokenize text (if provided)
        # Step 3: Extract image_features & text_features
        # Step 4: Apply fusion w_img * image_features + w_text * text_features
        # Step 5: Compute similarity against database representations

        # Dummy response logic for template
        dummy_results = [
            MatchResult(image_id="img_1001", score=0.98, description="Matching food image based on textual query"),
            MatchResult(image_id="img_1002", score=0.85, description="Secondary visual match")
        ]

        return dummy_results[:request.top_k]
