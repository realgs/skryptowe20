def model_to_dict(model):
    list_of_dict = {}
    for i in range(len(model)):
        dictionary = model[i]._asdict()
        list_of_dict[i] = dictionary
    return list_of_dict
