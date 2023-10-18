from owlready2 import *

onto_path.append("C:/Users/Beerstein/Documents/MIT/Thesis")

ontology = get_ontology("C:/Users/Beerstein/Documents/MIT/Thesis/urn_webprotege_ontology_8309ad70-dac3-42f8-b823-2b3b2c4f7b4e.owl").load()
ontology.load(only_local=True)

classes = list(ontology.classes())
object_props = list(ontology.object_properties())
data_props = list(ontology.data_properties())

print(classes)
print(object_props)
print(data_props)

test = data_props[0]
python_name = test._python_name
name = test.label[0]
comments = test.comment[0]
split_comment = comments.split('//')

x=1