export default {
    name: 'social-posts',
    template: '#social-posts-template',
    components: {
        'social-posts-compose': () => import(staticFiles + "vue/social-posts-compose.js"),
        'social-posts-item':  () => import(staticFiles + "vue/social-posts-item.js"),
    },
    data() {
        return {
            pageNum: 1,
            posts: null,
            hasNext: null,
            hasPrev: null,
            auth: auth
        }
    },
    created: function () {
        this.fetchPosts(this.pageNum)
    },
    methods: {
        fetchPosts: function (p) {
            if (this.$route.name === 'follow') {
                fetch(`/posts?page=${p}&follow=1`)
                .then(response => response.json())
                .then(result => {
                    this.posts = result.posts;
                    this.hasNext = result.has_next;
                    this.hasPrev = result.has_prev;
                })
            } else if (this.$route.name === 'profile') {
                fetch(`/posts?page=${p}&profile=${this.$route.params.id}`)
                .then(response => response.json())
                .then(result => {
                    this.posts = result.posts;
                    this.hasNext = result.has_next;
                    this.hasPrev = result.has_prev;
                })
            } else {
                fetch(`/posts?page=${p}`)
                .then(response => response.json())
                .then(result => {
                    this.posts = result.posts;
                    this.hasNext = result.has_next;
                    this.hasPrev = result.has_prev;
                })
            }
        }
    }
}
