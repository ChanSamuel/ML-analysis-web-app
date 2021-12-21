"""
The analysers package contains a collection of analyser modules.


Each analyser module provides the following:
 - Multiple analyse(Handler) function. Each analyse function typically performs some analysis
 and returns the result of such analysis. There exists an analyse(...) function for each Handler subtype;
 multiple dispatch is used to choose the correct analyse(...) function for the corresponding Handler subtype.
 - A supported_handlers() function which returns a list of Handler types which this analyser module can analyse for.
 - A supports(Handler) function, which simply returns whether the given Handler type is supported or not.



"""