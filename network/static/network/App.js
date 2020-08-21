var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        message: 'Hello Vue!',
    },
    methods: {
        greet: function() {
            return('Greetings to everytone!')
        }
    }
});

