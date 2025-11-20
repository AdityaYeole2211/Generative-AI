1. class State is a typedict object, can be imported from typing_extensions.

2. A TypedDict type represents dict objects that contain only keys of type str. 
There are restrictions on which string keys are valid, and which values can be associated with each key. 
Values that inhabit a TypedDict type must be instances of dict itself, not a subclass. You define a TypedDict by inheriting 
from typing.TypedDict and specifying the expected keys as class attributes with their respective type hints.

3. Every node is a function . Their input is a state and output is also a state. They update the state.
