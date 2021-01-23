export default {
    namespaced: true,
    state: {
        topicsList: [
            {

                topic: 'temat1',
                description: "opis1",
            },
            {

                topic: 'temat2',
                description: "opis2",
            },
            {

                topic: 'temat3',
                description: "opis3",
            },
            {

                topic: 'temat4',
                description: "opis4",
            }]
    },
    mutations: {
        setTopicsList(state, payload) {
            state.topicsList = payload
        }
    },
    actions: {
        getTopicsList({commit, state}) {
            // TODO axios
        }
    }
}