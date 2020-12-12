def model_to_dict(model):
    list_of_dict = {}
    for i in range(len(model)):
        dictionary = model[i].__dict__
        del dictionary["_sa_instance_state"]
        list_of_dict[i] = dictionary
    return list_of_dict
