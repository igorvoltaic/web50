Vue.config.ignoredElements = [/^ion-/]

new Vue({
    el: "#app",
    components: {
        navbar: NavbarComponent,
        'social-posts': SocialPostsComponent
    }
})
