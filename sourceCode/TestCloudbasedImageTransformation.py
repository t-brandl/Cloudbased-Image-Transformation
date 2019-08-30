import unittest
import cloudbasedImageTransformation

class TestCloudTransformationService(unittest.TestCase):
    
    def test_nourl(self):
        call = {"selected_mode" : 1, "image_url" : " "}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("message"), "URL is not valid")
        
    def test_wrongurl(self):
        call = {"selected_mode" : 1, "image_url" : "https://docs.python.org/3/library/unittest.html"}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("message"), "Image needs to be a jpg or png")
        
    def test_wrongMode(self):
        call = {"selected_mode" : 4, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("message"), "Not a valid mode selected")
        
    def test_blackwhite(self):
        call = {"selected_mode" : 1, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("statusCode"), 200)
    
    def test_upscale(self):
        call = {"selected_mode" : 2, "scale" : 2, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("statusCode"), 200)
        
    def test_upscale_noscale(self):
        call = {"selected_mode" : 2, "scale" : 2, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("statusCode"), 200)
        
    def test_cartoonify(self):
        call = {"selected_mode" : 3, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformationService(call)
        
        self.assertEqual(result.get("body").get("statusCode"), 200)

if __name__ == '__main__':
    unittest.main()