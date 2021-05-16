from bocr_71_api.constants import CLASSES,CHARACTER_CLASSIFIER_WEIGHT, top, bottom, left, right

import sys
sys.path.append('bocr_71_api/text_classifier/')
from yolo.detect import detect
from helpers.classes import Recognizer
from bocr_71_api.classifier_helper.classifier_helper import extractWordFromOutput as construct_word_from_characters
from bocr_71_api.text_classifier.helpers.utilities import constructAlphabetsBelongings

def get_text_from_image(image_src: str = None):
    if image_src is None: return []
    image_path = image_src or 'bocr_71_api/test.png'
    classifier = Recognizer(
        image=[image_path],
        weights= CHARACTER_CLASSIFIER_WEIGHT
    )
    characters = detect(classifier)[0]
    texts_from_characters = constructAlphabetsBelongings(characters, 
                                                        left=left, 
                                                        top = top, 
                                                        bottom = bottom, 
                                                        right = right)
    return construct_word_from_characters(texts_from_characters, classes=CLASSES)