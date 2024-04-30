document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".btn-delete").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const articleId = e.target.dataset.id;

      const response = await fetch(`/delete_article/${articleId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        window.location.reload();
      } else {
        console.log("Error deleting article");
      }
    });
  });
  const form = document.getElementById("new-article-form") || null;

  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const title = form.querySelector("#title").value;
      const content = form.querySelector("#content").value;
      const category = form.querySelector("#category").value;
      const status = e.submitter.className.includes("btn-success")
        ? "publish"
        : "draft";

      const articleData = {
        title,
        content,
        category,
        status,
      };
      try {
        const response = await fetch("/article", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(articleData),
        });

        if (response.ok) {
          window.location.href = "/article"; // Redirect to the article page
        } else {
          console.log("Error adding article");
        }
      } catch (error) {
        console.log("Network error:", error);
      }
    });
  }

  const editForm = document.getElementById("edit-article-form") || null;

  if (editForm) {
    editForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const title = editForm.querySelector("#title").value;
      const content = editForm.querySelector("#content").value;
      const category = editForm.querySelector("#category").value;
      const status = e.submitter.className.includes("btn-success")
        ? "draft"
        : "publish";
      const articleId = editForm.querySelector("input[name='id']").value;

      const articleData = {
        title,
        content,
        category,
        status,
      };

      console.log(articleData);

      try {
        const response = await fetch(`/article/${articleId}`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(articleData),
        });

        if (response.ok) {
          window.location.href = "/article"; // Redirect to main page
        } else {
          console.log("Error updating article");
        }
      } catch (error) {
        console.log("Network error:", error);
      }
    });
  }
});
