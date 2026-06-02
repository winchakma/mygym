with open('frontend/js/script.js', 'a', encoding='utf-8') as f:
    f.write("""
if (document.readyState === 'loading') {
    document.addEventListener("DOMContentLoaded", initSupportWidget);
} else {
    initSupportWidget();
}
""")
print("Fixed missing initSupportWidget call")
