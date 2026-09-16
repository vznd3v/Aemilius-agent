use pyo3::prelude::*;

// 1. On définit une fonction classique avec l'attribut #[pyfunction]
#[pyfunction]
fn saluer(nom: String) -> PyResult<String> {
    // PyResult est l'équivalent d'un try/except Python (gère les erreurs)
    Ok(format!("Bonjour {} depuis le monde Rust ! 🦀", nom))
    
}

// 2. On crée le module Python (le nom doit être EXACTEMENT le même que dans Cargo.toml)
#[pymodule]
fn _core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // On ajoute la fonction au module Python
    m.add_function(wrap_pyfunction!(saluer, m)?)?;
    Ok(())
}