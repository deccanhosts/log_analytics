# This make script should be invoked as super user
# Add your proto file to be checked in here
PROTOFILES= log_analytics.proto

all: clean createoutdir compile_proto clean
# inference rule
compile_proto: $(PROTOFILES)
	protoc --fastpython_out 'userapi:out' --cpp_out out/ $(PROTOFILES); \
	cd out; \
	python setup.py install; \
	cd ../..

createoutdir:
	mkdir -p out

clean:
	rm -rf out *.py *.pyc *.egg
