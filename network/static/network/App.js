Vue.config.ignoredElements = [/^ion-/]

new Vue({
    router,
    el: "#app",
    components: {
        navbar: NavbarComponent,
    }
})
