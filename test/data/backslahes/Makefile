# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html

var := one$\
       word

a: b \
	c
	echo "a"

b:
	echo "b"

c:
	echo "c"


# https://www.gnu.org/software/make/manual/html_node/Splitting-Recipe-Lines.html

all :
	@echo no\
space
	@echo no\
	space
	@echo one \
	space
	@echo one\
	 space

d : all
	echo "d"
