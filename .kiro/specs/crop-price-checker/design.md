# Design Document: Kisan-Sahayak (Crop Price Checker)

## Overview

Kisan-Sahayak is a Python-based command-line application that helps rural Indian farmers check current crop prices in their local language. The system uses mock data to simulate market prices and provides expert advice, with AI-powered translation supporting English, Tamil, and Hindi.

The application is designed for simplicity and accessibility, targeting users with limited technical knowledge. It operates entirely offline using the deep-translator library for language support and simulates realistic market price variations using Python's Random module.

## Architecture

The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Interface                         │
│  (User Input/Output, Menu Display, Session Management)  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│                 Application Controller                   │
│     (Orchestrates flow between components)              │
└────┬──────────────────────────────────┬─────────────────┘
     │                                   │
     ▼                                   ▼
┌─────────────────────┐      ┌──────────────────────────┐
│  Price Service      │      │  Translation Service     │
│  - Get crop price   │      │  - Translate text        │
│  - Get advice       │      │  - Language selection    │
│  - Mock data mgmt   │      │  - Fallback handling     │
└─────────────────────┘      └──────────────────────────┘
```

Design Rationale:
- Layered architecture separates UI concerns from business logic
- Service-based design allows easy testing and future extensibility
- Translation service is isolated to handle failures independently
- Mock data approach eliminates external dependencies for reliability

## Components and Interfaces

### 1. CLI Interface Module

Handles all user interaction through the command line.

```python
class CLIInterface:
    def display_welcome() -> None
    def display_menu() -> None
    def get_user_choice() -> str
    def get_crop_name() -> str
    def display_price_info(crop: str, price: float, advice: str) -> None
    def display_error(message: str) -> None
    def display_goodbye() -> None
```

Responsibilities:
- Display formatted text to users
- Capture and validate user input
- Present menu options and results
- Handle display of translated content

### 2. Translation Service

Manages language selection and text translation using deep-translator.

```python
class TranslationService:
    def __init__(self):
        self.current_language: str
        self.translator: GoogleTranslator
    
    def select_language() -> str
    def translate(text: str, target_lang: str) -> str
    def set_language(language: str) -> None
    def get_current_language() -> str
```

Responsibilities:
- Initialize deep-translator library
- Translate text between English, Tamil, and Hindi
- Maintain current language selection throughout session
- Implement fallback to English on translation failure

Design Rationale:
- GoogleTranslator from deep-translator chosen for broad language support
- Fallback mechanism ensures application never crashes due to translation errors
- Language state maintained in service to avoid passing it everywhere

### 3. Price Service

Manages crop price data and expert advice with simulated variations.

```python
class PriceService:
    def __init__(self):
        self.crop_database: Dict[str, CropData]
    
    def get_price(crop_name: str) -> float
    def get_advice(crop_name: str) -> str
    def is_valid_crop(crop_name: str) -> bool
    def get_supported_crops() -> List[str]
    def _apply_price_variation(base_price: float) -> float
```

```python
@dataclass
class CropData:
    name: str
    base_price: float  # Price per quintal in INR
    advice: str
```

Responsibilities:
- Store and retrieve crop price data
- Apply ±10% random variation to simulate market fluctuations
- Provide expert advice for each crop
- Validate crop names against supported list

Design Rationale:
- Dictionary-based storage for O(1) crop lookup
- Random variation applied at query time to simulate dynamic markets
- Base prices stored separately from displayed prices for consistency
- Minimum 5 crops supported: Rice, Wheat, Cotton, Sugarcane, Maize

### 4. Application Controller

Orchestrates the main application flow and coordinates between services.

```python
class ApplicationController:
    def __init__(self):
        self.price_service: PriceService
        self.translation_service: TranslationService
        self.cli: CLIInterface
        self.running: bool
    
    def initialize() -> None
    def run() -> None
    def handle_price_check() -> None
    def handle_exit() -> None
    def _translate_and_display(text: str) -> None
```

Responsibilities:
- Initialize all services and mock data
- Manage main application loop
- Route user actions to appropriate services
- Handle errors and coordinate fallback behavior

## Data Models

### Crop Database Structure

```python
CROP_DATABASE = {
    "rice": CropData(
        name="Rice",
        base_price=2000.0,  # INR per quintal
        advice="Rice prices are stable. Consider selling after monsoon for better rates."
    ),
    "wheat": CropData(
        name="Wheat",
        base_price=2500.0,
        advice="Wheat demand is high in winter months. Store in dry conditions."
    ),
    "cotton": CropData(
        name="Cotton",
        base_price=6000.0,
        advice="Cotton prices fluctuate with global demand. Monitor market trends."
    ),
    "sugarcane": CropData(
        name="Sugarcane",
        base_price=3000.0,
        advice="Sell to nearby sugar mills for best prices. Harvest timing is critical."
    ),
    "maize": CropData(
        name="Maize",
        base_price=1800.0,
        advice="Maize has steady demand. Consider selling in smaller batches."
    )
}
```

### Language Mapping

```python
LANGUAGE_CODES = {
    "english": "en",
    "tamil": "ta",
    "hindi": "hi"
}
```

## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.


### Property 1: Valid crop queries return complete information
*For any* valid crop name, querying the system should return both a price value and expert advice text.
**Validates: Requirements 1.1, 2.1**

### Property 2: Price display format consistency
*For any* crop price query result, the displayed output should include the unit "per quintal" and "INR" or "Rupees".
**Validates: Requirements 1.4**

### Property 3: Advice always provided
*For any* crop query (whether specific advice exists or not), the system should return non-empty advice text.
**Validates: Requirements 2.3**

### Property 4: Language consistency throughout session
*For any* user session with a selected language, all system outputs should remain in that selected language across multiple operations.
**Validates: Requirements 3.2, 3.5**

### Property 5: Translation failure fallback
*For any* translation failure, the system should display the original English text and continue operating.
**Validates: Requirements 3.4, 6.2**

### Property 6: Multiple operations without restart
*For any* sequence of valid crop queries, the system should process all queries without requiring restart or termination.
**Validates: Requirements 4.4**

### Property 7: Price variation within bounds
*For any* crop, querying its price multiple times should produce values that vary by no more than ±10% from the base price.
**Validates: Requirements 5.4**

### Property 8: Price variation occurs
*For any* crop, querying its price at least 10 times should produce at least 2 different price values (demonstrating variation).
**Validates: Requirements 5.2**

### Property 9: Invalid input error handling
*For any* invalid input (invalid crop name, invalid menu choice, etc.), the system should display an error message and continue running.
**Validates: Requirements 1.2, 6.1**

### Property 10: Initialization performance
*For any* application launch, the system should complete initialization and display the main menu within 3 seconds.
**Validates: Requirements 7.1**

### Property 11: Missing dependency error handling
*For any* missing required library, the system should display a clear error message identifying the missing dependency.
**Validates: Requirements 7.4**

## Error Handling

The application implements a multi-layered error handling strategy:

### Input Validation Layer
- All user inputs validated before processing
- Invalid crop names checked against supported crop list
- Menu choices validated against available options
- Empty or whitespace-only inputs rejected with helpful messages

### Translation Error Handling
- Try-catch blocks around all translation calls
- Automatic fallback to English on translation failure
- Error logging for debugging without disrupting user experience
- Graceful degradation: app remains functional even if translation fails

### Service-Level Error Handling
- Price Service validates crop names before lookup
- Returns None for invalid crops, allowing caller to handle appropriately
- Translation Service catches deep-translator exceptions
- All services designed to never crash the application

### Application-Level Error Handling
- Top-level exception handler in main loop prevents crashes
- Unexpected errors logged with full stack trace
- User shown friendly error message and returned to menu
- Application state preserved across errors

Design Rationale:
- Defense in depth: multiple layers catch different error types
- Fail gracefully: never crash, always return to usable state
- User-friendly: technical errors translated to helpful messages
- Debuggable: all errors logged for troubleshooting

## Testing Strategy

The application will use a dual testing approach combining unit tests and property-based tests to ensure comprehensive coverage.

### Unit Testing Approach

Unit tests will verify specific examples, edge cases, and integration points:

- **CLI Interface Tests**: Verify menu display, input capture, output formatting
- **Translation Service Tests**: Test language selection, specific translations, fallback behavior
- **Price Service Tests**: Verify crop lookup, advice retrieval, supported crop list
- **Application Controller Tests**: Test initialization, main loop, error coordination
- **Integration Tests**: Verify end-to-end flows (startup → language selection → price check → exit)

Focus areas for unit tests:
- Specific examples demonstrating correct behavior (e.g., querying "Rice" returns expected format)
- Edge cases (empty input, special characters, very long crop names)
- Error conditions (missing dependencies, translation failures, invalid inputs)
- Startup and shutdown sequences

### Property-Based Testing Approach

Property-based tests will verify universal properties across many generated inputs using the **Hypothesis** library for Python.

Each correctness property listed above will be implemented as a property-based test:
- Minimum 100 iterations per test to ensure thorough coverage
- Random generation of crop names, user inputs, and session sequences
- Each test tagged with format: **Feature: crop-price-checker, Property N: [property text]**

Property test generators:
- Valid crop names: randomly select from supported crop list
- Invalid crop names: generate random strings not in supported list
- User sessions: generate sequences of valid operations
- Language selections: randomly choose from English, Tamil, Hindi

Design Rationale:
- Unit tests catch specific bugs and verify concrete examples
- Property tests verify correctness across the entire input space
- Hypothesis handles edge case generation automatically
- 100+ iterations per property ensure statistical confidence
- Together, both approaches provide comprehensive validation

### Test Configuration

```python
# Property-based test configuration
from hypothesis import given, settings, strategies as st

@settings(max_examples=100)
@given(crop_name=st.sampled_from(["rice", "wheat", "cotton", "sugarcane", "maize"]))
def test_property_1_valid_crop_returns_complete_info(crop_name):
    """Feature: crop-price-checker, Property 1: Valid crop queries return complete information"""
    # Test implementation
    pass
```

## Implementation Notes

### Technology Stack
- **Language**: Python 3.8+
- **Translation**: deep-translator library (GoogleTranslator)
- **Testing**: pytest for unit tests, Hypothesis for property-based tests
- **Random**: Python standard library Random module

### Dependencies
```
deep-translator>=1.9.0
pytest>=7.0.0
hypothesis>=6.0.0
```

### Project Structure
```
kisan-sahayak/
├── src/
│   ├── __init__.py
│   ├── cli_interface.py
│   ├── translation_service.py
│   ├── price_service.py
│   ├── application_controller.py
│   └── models.py
├── tests/
│   ├── __init__.py
│   ├── test_cli_interface.py
│   ├── test_translation_service.py
│   ├── test_price_service.py
│   ├── test_application_controller.py
│   └── test_properties.py
├── main.py
├── requirements.txt
└── README.md
```

### Key Design Decisions

1. **Mock Data Over External APIs**: Using internal mock data ensures reliability and offline operation, critical for rural areas with limited connectivity.

2. **Deep-Translator Library**: Chosen for its simplicity and support for multiple translation engines. GoogleTranslator backend provides good quality for Tamil and Hindi.

3. **Random Price Variation**: ±10% variation simulates realistic market fluctuations without requiring real-time data feeds.

4. **Service-Based Architecture**: Separating concerns into services makes the codebase testable, maintainable, and extensible for future enhancements.

5. **Fallback to English**: Ensures application remains usable even when translation fails, prioritizing functionality over perfect localization.

6. **Command-Line Interface**: Chosen for simplicity and accessibility on low-resource systems. No GUI dependencies required.

7. **Session-Based Language**: Language selected once per session reduces complexity and matches typical usage patterns.

8. **Hypothesis for Property Testing**: Industry-standard library with excellent Python support and automatic edge case generation.
