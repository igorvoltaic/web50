// Update watchlist elements onClick over the button adding number of
// watched items on top and changing text for watched item

const watchNum = document.querySelector('#watchlist-num');
const addWatchlist = document.querySelector('#add-watchlist');
document.addEventListener('DOMContentLoaded', function() {
    addWatchlist.onclick = function() {
        event.preventDefault()
        fetch('http://127.0.0.1:8000/add-watchlist/' + listingId)
        .then(response => response.json())
        .then(data => {
            const inWatchlist = data.inwl
            if (!inWatchlist) {
                addWatchlist.classList = "watchlist active-wl";
                addWatchlist.text = "watching";
                if (Number(watchNum.textContent) > 0) {
                    watchNum.textContent = Number(watchNum.textContent) + 1;
                } else {
                    watchNum.classList = "watchlist active-wl";
                    watchNum.innerText = "1";
                }
            } else {
                addWatchlist.classList = "watchlist inactive-wl";
                addWatchlist.text = "to watchlist";
                if (Number(watchNum.textContent) > 1 ) {
                    watchNum.textContent = Number(watchNum.textContent) - 1;
                } else {
                    watchNum.classList = ""
                    watchNum.innerText = "";
                }
            }
        });
    }
});
