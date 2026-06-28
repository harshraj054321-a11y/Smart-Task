


// ---------- Smooth Button Animation ----------

const buttons = document.querySelectorAll(".btn");

buttons.forEach(button => {

    button.addEventListener("mouseenter", function () {
        this.style.transform = "translateY(-3px)";
    });

    button.addEventListener("mouseleave", function () {
        this.style.transform = "translateY(0)";
    });

});


// ---------- Auto Hide Django Messages ----------

const messages = document.querySelectorAll(".alert");

messages.forEach(message => {

    setTimeout(() => {

        message.style.transition = "0.5s";
        message.style.opacity = "0";

        setTimeout(() => {
            message.remove();
        }, 500);

    }, 3000);

});


// ---------- Scroll Animation ----------

const cards = document.querySelectorAll(".task-card, .stat-card, .progress-card");

const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {

        if (entry.isIntersecting) {

            entry.target.style.opacity = "1";
            entry.target.style.transform = "translateY(0)";

        }

    });

});

cards.forEach(card => {

    card.style.opacity = "0";
    card.style.transform = "translateY(20px)";
    card.style.transition = "0.6s ease";

    observer.observe(card);

});