import log_analytics_proto

def buildProto():
 """Test protocol buffer serialization."""
req_payload = log_analytics_proto.req_payload_struct(hostname = "testing1.dev.deccanhosts.com",
                                                    time_from = 1349340137)
req_msg = log_analytics_proto.req_msg(req_id      = "test_id",\
                                      req_type    = 1,
                                      req_payload = req_payload)
wire_str = req_msg.SerializeToString()
print "serialized request:: \n", wire_str
open("tmp_get_test.txt", "wb").write(wire_str)

if __name__ == "__main__":
  buildProto()

