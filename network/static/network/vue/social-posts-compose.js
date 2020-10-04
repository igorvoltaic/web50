export default {
    name: 'social-posts-compose',
    delimiters: ['[[',']]'],
    template: '#social-posts-compose-template',
    data() {
        return {
            isNewPost: false,
            post: {
                body: ''
            }
        }
    },
    methods: {
        newPost: function() {
            fetch('/posts', {
                method: 'POST',
                credentials: 'same-origin',
                headers: {
                    "X-CSRFToken": csrf_token
                },
                body: JSON.stringify({
                    body: this.post.body
                })
            })
            .then(response => response.json())
            .then(result => {
                this.$parent.fetchPosts("1")
                this.isNewPost = false
                this.post.body = ''
            });

            // Prevent default submission
            return false;
        },
    }
}

