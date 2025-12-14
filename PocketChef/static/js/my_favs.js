document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('recipes-container');
    const tabs = document.querySelector('.sort-tabs');
    const searchInput = document.getElementById('filter-search');
    const areaSelect = document.getElementById('filter-area');
    const categorySelect = document.getElementById('filter-category');
    const clearBtn = document.getElementById('filter-clear');
    const resultsCount = document.getElementById('results-count');

    let mealsData = [];
    let activeSort = 'random';

    
    let currentUser = null;
    try {
        const el = document.getElementById('user-data');
        if (el) {
            const txt = el.textContent.trim() || 'null';
            currentUser = JSON.parse(txt);
        }
    } catch (e) {
        currentUser = null;
    }
    const isLoggedIn = !!(currentUser && currentUser.email);

    let favorites = new Set();

        function loadFavorites() {
        // not logged in -> use localStorage only
        if (!isLoggedIn) {
            favorites = new Set(JSON.parse(localStorage.getItem('favoriteMeals') || '[]'));
            return Promise.resolve();
        }

        // logged in -> load from backend
        return fetch('/api/favorites')
            .then(r => {
                if (!r.ok) {
                    throw new Error('Favorites API returned ' + r.status);
                }
                return r.json();
            })
            .then(rows => {
                favorites = new Set(rows.map(r => String(r.meal_id)));
            })
            .catch(() => {
                favorites = new Set();
            });
    }

    function saveFavoritesLocal() {
        if (!isLoggedIn) {
            localStorage.setItem('favoriteMeals', JSON.stringify(Array.from(favorites)));
        }
    }

    function shuffle(arr) {
        for (let i = arr.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }

    function createCard(meal) {
        const div = document.createElement('div');
        const id = String(meal.idMeal);

        div.className = 'recipe-card';
        div.innerHTML = `
            <button class="fav-btn is-fav" type="button" aria-label="Remove favourite">
                ♥
            </button>
            <img src="${meal.strMealThumb}" alt="${meal.strMeal}" loading="lazy">
            <div class="card-body">
                <div>
                    <h3>${meal.strMeal}</h3>
                    <p class="meta">${meal.strArea || 'Unknown'} • ${meal.strCategory || 'Uncategorized'}</p>
                </div>
                <div class="view-note">Click the card to view details on TheMealDB</div>
            </div>
        `;

        // open TheMealDB on card click
        div.addEventListener('click', () => {
            window.open(`https://www.themealdb.com/meal.php?c=${id}`, '_blank');
        });

        // remove from favourites
        const favBtn = div.querySelector('.fav-btn');
        favBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            fetch(`/api/favorites/${id}`, { method: 'DELETE' })
                .then(res => {
                    if (!res.ok) throw new Error('Failed favourite update');
                    div.remove();
                    updateCount();
                    if (!container.querySelector('.recipe-card')) {
                        container.textContent = 'You have no favourite recipes yet.';
                    }
                })
                .catch(err => console.error(err));
        });

        container.appendChild(div);
    }

    function updateCount() {
        const n = container.querySelectorAll('.recipe-card').length;
        resultsCount.textContent = `${n} favourite(s)`;
    }

    function loadFavorites() {
        fetch('/api/favorites')
            .then(r => {
                if (!r.ok) throw new Error('Favorites API returned ' + r.status);
                return r.json();
            })
            .then(rows => {
                if (!rows.length) {
                    resultsCount.textContent = '0 favourite(s)';
                    container.textContent = 'You have no favourite recipes yet.';
                    return;
                }

                const ids = rows.map(r => r.meal_id);
                return Promise.all(
                    ids.map(id =>
                        fetch(`https://www.themealdb.com/api/json/v1/1/lookup.php?i=${id}`)
                            .then(r => r.json())
                            .then(d => (d.meals && d.meals[0]) || null)
                    )
                ).then(meals => {
                    const valid = meals.filter(Boolean);
                    valid.forEach(createCard);
                    updateCount();
                });
            })
            .catch(err => {
                console.error(err);
                container.textContent = 'Failed to load favourite recipes.';
            });
    }

    loadFavorites();


        container.appendChild(div);
    

    function applyFilters(list) {
        const q = (searchInput.value || '').trim().toLowerCase();
        const area = areaSelect.value;
        const category = categorySelect.value;
        return list.filter(m => {
            if (q && !(m.strMeal || '').toLowerCase().includes(q)) return false;
            if (area && (m.strArea || '') !== area) return false;
            if (category && (m.strCategory || '') !== category) return false;
            return true;
        });
    }

    function renderMeals() {
        container.innerHTML = '';
        if (!mealsData || !mealsData.length) {
            resultsCount.textContent = '';
            container.textContent = 'No recipes found.';
            return;
        }
        const filtered = applyFilters(mealsData.slice());

        switch (activeSort) {
            case 'name-asc':
                filtered.sort((a, b) => (a.strMeal || '').localeCompare(b.strMeal || ''));
                break;
            case 'name-desc':
                filtered.sort((a, b) => (b.strMeal || '').localeCompare(a.strMeal || ''));
                break;
            case 'area':
                filtered.sort((a, b) => (a.strArea || '').localeCompare(b.strArea || ''));
                break;
            case 'category':
                filtered.sort((a, b) => (a.strCategory || '').localeCompare(b.strCategory || ''));
                break;
            case 'random':
            default:
                shuffle(filtered);
                break;
        }

        resultsCount.textContent = `Showing ${Math.min(filtered.length, 16)} of ${filtered.length} result(s)`;

        if (filtered.length === 0) {
            container.textContent = 'No recipes match your filters.';
            return;
        }

        filtered.slice(0, 16).forEach(createCard);
    }

    function populateFilters() {
        const areas = Array.from(new Set(mealsData.map(m => m.strArea).filter(Boolean))).sort();
        const cats = Array.from(new Set(mealsData.map(m => m.strCategory).filter(Boolean))).sort();
        function fill(select, items) {
            select.querySelectorAll('option:not([value=""])').forEach(o => o.remove());
            items.forEach(it => {
                const opt = document.createElement('option');
                opt.value = it;
                opt.textContent = it;
                select.appendChild(opt);
            });
        }
        fill(areaSelect, areas);
        fill(categorySelect, cats);
    }

    // fetch and initialize
    Promise.all([
        fetch('https://www.themealdb.com/api/json/v1/1/search.php?s=').then(r => r.json()),
        loadFavorites()
    ])
        .then(([data]) => {
            mealsData = data.meals || [];
            populateFilters();
            renderMeals();
        })
        .catch(() => {
            container.textContent = 'Failed to load recipes.';
        });

    // tab/tap handling
    if (tabs) {
        tabs.addEventListener('click', (e) => {
            const btn = e.target.closest('button[data-sort]');
            if (!btn) return;
            activeSort = btn.dataset.sort;
            tabs.querySelectorAll('button').forEach(b => b.classList.toggle('active', b === btn));
            renderMeals();
        });
    }

    // filter events
    [searchInput, areaSelect, categorySelect].forEach(el => {
        if (!el) return;
        el.addEventListener('input', () => renderMeals());
        el.addEventListener('change', () => renderMeals());
    });

    if (clearBtn && tabs) {
        clearBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            if (areaSelect) areaSelect.value = '';
            if (categorySelect) categorySelect.value = '';
            activeSort = 'random';
            tabs.querySelectorAll('button').forEach(
                b => b.classList.toggle('active', b.dataset.sort === 'random')
            );
            renderMeals();
        });
    }
});
