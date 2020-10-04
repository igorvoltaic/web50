export default {
    template: '#navbar-template',
    components: {
        'navbar-link': () => import(staticFiles + "vue/navbar-link.js")
    },
    data() {
        return {
            links: navLinks,
            isFollowing: false,
            isActive: false
        }
    }
}
