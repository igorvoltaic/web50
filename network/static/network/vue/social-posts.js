export default {
    name: 'social-posts',
    template: '#social-posts-template',
    components: {
        'social-posts-compose': () => import(staticFiles + "vue/social-posts-compose.js"),
        'social-posts-item':  () => import(staticFiles + "vue/social-posts-item.js"),
    },
    props: {
        isFollowing: {
            default: false,
            type: Boolean
        },
        doFetchPosts: {
            default: false,
            type: Boolean
        },
        isProfile: {
            default: '',
            type: String
        },

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
            if (this.isFollowing) {
                fetch(`/posts?page=${p}&follow=1`)
                .then(response => response.json())
                .then(result => {
                    this.posts = result.posts;
                    this.hasNext = result.has_next;
                    this.hasPrev = result.has_prev;
                })
            } else if (this.isProfile) {
                fetch(`/posts?page=${p}&profile=${this.isProfile}`)
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
