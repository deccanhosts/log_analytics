import log_analytics_proto

def buildProto():
 """Test protocol buffer serialization."""
req_msg = log_analytics_proto.req_msg(req_id = "test_id",\
                                        hostname = "testing1.dev.deccanhosts.com",\
                                        time_from = 1349340137)
wire_str = req_msg.SerializeToString()
print "serialized request:: \n", wire_str
open("tmp_get_test.txt", "wb").write(wire_str)

if __name__ == "__main__":
  buildProto()

