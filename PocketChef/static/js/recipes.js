document.addEventListener('DOMContentLoaded', function() {
    // Example: Get 10 random meals from TheMealDB
    fetch('https://www.themealdb.com/api/json/v1/1/search.php?s=')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('recipes-container');
            if (!data.meals) {
                container.textContent = 'No recipes found.';
                return;
            }
            data.meals.slice(0, 16).forEach(meal => {
                const div = document.createElement('div');
                div.className = 'recipe-card';
                div.innerHTML = `
                    <h2>${meal.strMeal}</h2>
                    <img src="${meal.strMealThumb}" alt="${meal.strMeal}" width="200">
                    <p>${meal.strArea} - ${meal.strCategory}</p>
                `;
                container.appendChild(div);
            });
        })
        .catch(() => {
            document.getElementById('recipes-container').textContent = 'Failed to load recipes.';
        });
});
