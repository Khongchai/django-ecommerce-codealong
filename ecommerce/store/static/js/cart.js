const updateButtons = document.getElementsByClassName("update-cart");

if (updateButtons.length > 0) {
  for (i = 0, length = updateButtons.length; i < length; i++) {
    /**
     * By using function(){} instead of the () => {} syntax, you can refer to the object
     * it belongs to as this.
     *
     * This in the anonymous function syntax refers to the global scope.
     */
    updateButtons[i].addEventListener("click", function () {
      const productId = this.dataset.product;
      const action = this.dataset.action;
      if (user === "AnonymousUser") {
        addCookieItem(productId, action);
      } else {
        updateUserOrder(productId, action);
      }
    });
  }
}

/**
 *
 * @param {number} productId
 * @param {"add" | "remove"} action
 */
function addCookieItem(productId, action) {
  console.log("not logged in");
}

/**
 *
 * @param {number} productId
 * @param {"add" | "remove"} action
 */
function updateUserOrder(productId, action) {
  const url = "/update_item/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({
      productId,
      action,
    }),
  })
    .then((response) => {
      return response.json();
    })
    .then(() => {
      //Force reload to update cart count. Primitive solution, but saves a lotta time.
      location.reload();
    });
}
