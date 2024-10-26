// Carrosel Slides
const slides = document.getElementById('carousel-slides');
const totalSlides = slides.children.length;
let currentIndex = 0;

document.getElementById('nextSlide').addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % totalSlides;
        updateSlidePosition();
});

document.getElementById('prevSlide').addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + totalSlides) % totalSlides;
        updateSlidePosition();
});

function updateSlidePosition() {
        slides.style.transform = `translateX(-${currentIndex * 100}%)`;
}