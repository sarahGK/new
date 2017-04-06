import unittest
from model import parse,parse_req,top_k 

class TestCase(unittest.TestCase):
  
  def test_parse_req(self):
    request = "GET /images/NASA-logosmall.gif align=left HTTP/1.0"
    self.assertEqual(parse_req(request),"/images/NASA-logosmall.gif align=left")
    request1 = "k\x83\xfb\x03tx\x83\xfb\x04tG\x83\xfb\x07t\xcd\x83\xfb"
    self.assertEqual(parse_req(request1),request1)
    r2 = "GET / history/apollo/apollo-13"
    self.assertEqual(parse_req(r2),"/ history/apollo/apollo-13")
    r3 = ""
    self.assertEqual(parse_req(r3),"")
    r4 = "/ history/apollo/apollo-13 HTTP/1.0"
    self.assertEqual(parse_req(r4),"/ history/apollo/apollo-13")

  def test_parse(self):
    line = '163.205.23.71 - - [26/Jul/1995:15:50:35 -0400] "HEAD /images/ksclogo-medium.gif HTTP/1.0" 200 0'
    host = parse(line,"host")
    self.assertEqual(host,'163.205.23.71')
    self.assertEqual(parse(line,"time"),'26/Jul/1995:15:50:35 -0400')
    self.assertEqual(parse(line,"request"),'HEAD /images/ksclogo-medium.gif HTTP/1.0')
    self.assertEqual(parse(line,"rcode"),'200')
    self.assertEqual(parse(line,"rbyte"),0)
    l1 = 'fbrown.gsfc.nasa.gov - - [26/Jul/1995:08:11:47 -0400] "GET /shuttle/resources/orbiters/endeavour.html>" 404 -'
    request,byte = parse(l1,'request','rbyte')
    self.assertEqual(request,'GET /shuttle/resources/orbiters/endeavour.html>')
    self.assertEqual(byte,0)
    
  def test_top_k(self):
    dict = {"A":1,
            "B":10,
            "C":5,
            "D":3,
            "E":6
        }
    top_3 = [[10,"B"],[6,"E"],[5,"C"]]

    self.assertEqual(top_k(dict,3),top_3)



if __name__ == '__main__':
  unittest.main()

