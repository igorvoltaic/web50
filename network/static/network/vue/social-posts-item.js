export default {
    name: 'social-posts-item',
    delimiters: ['[[',']]'],
    template: '#social-posts-item-template',
    props: ['post'],
    data() {
        return {
            isEditing: false,
            isLiked: this.post.liked,
            currentUser: currentUser,
            auth: auth
        }
    },
    methods: {
        save: function () {
            this.post.body = this.$refs['post_body'].value,
            this.isEditing = !this.isEditing
            fetch(`/posts/${this.post.id}`, {
                method: 'PUT',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                body: JSON.stringify({
                    body: this.post.body
                })
            })
        },
        like: function () {
            if (auth) {
                if (this.isLiked) {
                    this.post.likes--
                    fetch(`/posts/${this.post.id}`, {
                        method: 'PUT',
                        credentials: 'same-origin',
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        body: JSON.stringify({
                            unlike: true
                        })
                    })
                } else {
                    this.post.likes++
                    fetch(`/posts/${this.post.id}`, {
                        method: 'PUT',
                        credentials: 'same-origin',
                        headers: {
                            "X-CSRFToken": csrf_token
                        },
                        body: JSON.stringify({
                            like: true
                        })
                    })
                }
                this.isLiked = !this.isLiked
            }
        }
    }
}
