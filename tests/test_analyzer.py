from services.sentiment_analyzer import sentiment_analyzer
import logging

logger = logging.getLogger(__name__)

def test_sentiment_analysis():
    """Tests sentiment analysis"""
    logger.info("Test: sentiment analysis")
    
    if not sentiment_analyzer.is_trained:
        logger.error("The model is not trained")
        return False
    
    test_cases = [
        {
            'text': 'I absolutely love this product, it is amazing!',
            'expected': 'positive',
            'description': 'Clearly positive text'
        },
        {
            'text': 'This is terrible, worst experience ever',
            'expected': 'negative',
            'description': 'Clearly negative text'
        },
        {
            'text': 'It is okay, nothing special',
            'expected': 'neutral',
            'description': 'Neutral text'
        },
        {
            'text': 'Excellent service, highly recommend!',
            'expected': 'positive',
            'description': 'Positive text'
        },
        {
            'text': 'Horrible quality, very disappointed',
            'expected': 'negative',
            'description': 'Negative text'
        }
    ]
    
    correct = 0
    total = len(test_cases)
    
    logger.info(f"\nAnalyzing {total} test texts...")
    logger.info("   " + "-"*50)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            result = sentiment_analyzer.analyze(test_case['text'])
            
            predicted = result['sentiment']
            confidence = result['confidence']
            
            is_correct = predicted == test_case['expected']
            if is_correct:
                correct += 1
                status = "✓"
            else:
                status = "✗"
            
            logger.info(f"   {status} Caso {i}: {test_case['description']}")
            logger.info(f"      Text: '{test_case['text'][:50]}...'")
            logger.info(f"      Expected: {test_case['expected']} | Predicted: {predicted}")
            logger.info(f"      Confidence: {confidence:.2%}")
            logger.info("")
            
        except Exception as e:
            logger.error(f"Error analyzing test case {i}: {e}")
            return False
    
    accuracy = (correct / total) * 100
    logger.info("   " + "-"*50)
    logger.info(f"Precision in test cases: {accuracy:.1f}% ({correct}/{total} corrects)")
    
    logger.info("\nAnalysis test in batches...")
    batch_texts = [tc['text'] for tc in test_cases[:3]]
    
    try:
        batch_results = sentiment_analyzer.analyze_batch(batch_texts)
        if len(batch_results) == len(batch_texts):
            logger.info(f"Analysis in batches ({len(batch_results)} texts)")
        else:
            logger.error("Error analysis in batches")
            return False
    except Exception as e:
        logger.error(f"Error analysis in batches: {e}")
        return False
    
    logger.info("\n   Model info:")
    model_info = sentiment_analyzer.get_model_info()
    logger.info(f"      Classes: {model_info.get('classes', [])}")
    logger.info(f"      Caracteristics: {model_info.get('n_features', 'N/A')}")
    logger.info(f"      Kernel: {model_info.get('kernel', 'N/A')}")
    
    logger.info("")
    return accuracy >= 60 