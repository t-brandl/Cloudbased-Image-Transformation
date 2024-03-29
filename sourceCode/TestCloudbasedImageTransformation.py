import unittest
import cloudbasedImageTransformation

class TestCloudTransformationService(unittest.TestCase):
    
    def test_nojsonInput(self):
        call = {}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("statusCode"), 405)
    
    def test_nourl(self):
        call = {"selected_mode" : 1, "image_url" : " "}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("message"), "URL is not valid")
        
    def test_wrongurl(self):
        call = {"selected_mode" : 1, "image_url" : "https://docs.python.org/3/library/unittest.html"}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("message"), "Image needs to be a jpg or png")
        
    def test_wrongMode(self):
        call = {"selected_mode" : 4, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("message"), "Not a valid mode selected")
        
    def test_blackwhite(self):
        call = {"selected_mode" : 1, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("statusCode"), 200)
    
    def test_upscale(self):
        call = {"selected_mode" : 2, "scale" : 2, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("statusCode"), 200)
        
    def test_upscale_noscale(self):
        call = {"selected_mode" : 2, "scale" : 2, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("statusCode"), 200)
        
    def test_cartoonify(self):
        call = {"selected_mode" : 3, "image_url" : "https://i.imgur.com/J4OKX3q.png"}
        result = cloudbasedImageTransformation.transformation_service(call)
        
        self.assertEqual(result.get("statusCode"), 200)

if __name__ == '__main__':
    unittest.main()