Vue.config.ignoredElements = [/^ion-/]

var navbar = new Vue({
    delimiters: ['[[', ']]'],
    el: '#navbar',
    data: {
        navLinks: navLinks,
        menuActive: false
    },
    methods: {
        slice: function(s) {
            return(s.slice(0,1))
        },
        setMenuActive: function() {
            this.menuActive = !this.menuActive;
        }
    }
});
