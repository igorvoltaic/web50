export default {
    delimiters: ['[[',']]'],
    template: '#user-profile-template',
    components: {
        'social-posts': () => import(staticFiles + "vue/social-posts.js")
    },
    props: {
        doFetchProfile: {
            default: false,
            type: Boolean
        },
    },
    data() {
        return {
            followersCount: null,
            followersNames: null,
            followCount: null,
            followNames: null,
            validFollow: null,
            isFollowed: null,
            username: null
        }
    },
    created: function () {
        this.fetchProfile(this.$route.params.id)
    },
    methods: {
        fetchProfile: function(user_id) {
            fetch(`/profile/${user_id}`)
            .then(response => response.json())
            .then(result => {
                this.username = result.username
                this.followersCount = result.followers_count
                this.followersNames = result.followers_names
                this.followCount = result.follow_count
                this.followNames = result.follow_names
                this.validFollow = result.valid_follow
                this.isFollowed = result.is_followed
            });
        },
        followUser: function () {
            fetch(`/profile/${this.$route.params.id}`, {
                method: 'PUT',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": csrf_token
                }
            })
            .then(result => {
                    this.fetchProfile(this.$route.params.id)
            })
        }
    }
}

