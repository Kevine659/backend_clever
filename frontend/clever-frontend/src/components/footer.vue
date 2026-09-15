<script setup>
</script>

<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-top">
        <div class="row gy-4">
          <div class="col-lg-4 col-md-6">
            <div class="footer-brand">
              <h3>CLEVER</h3>
              <p>
                Votre boutique spécialisée dans des produits
                cosmétiques,santé et diététique.
              </p>
              <div class="social-links">
                <a href="#" aria-label="Facebook">
                  <i class="bi bi-facebook"></i>
                </a>
                <a href="#" aria-label="Instagram">
                  <i class="bi bi-instagram"></i>
                </a>
                <a href="#" aria-label="TikTok">
                  <i class="bi bi-tiktok"></i>
                </a>
                <a href="#" aria-label="WhatsApp">
                  <i class="bi bi-whatsapp"></i>
                </a>
              </div>
            </div>
          </div>
          <div class="col-lg-2 col-md-6 col-6">
            <div class="footer-column">
              <h4>Boutique</h4>
              <ul>
                <li>
                  <RouterLink to="/">Accueil</RouterLink>
                </li>
                <li>
                  <RouterLink to="/produits">Produits</RouterLink>
                </li>
                <li>
                  <RouterLink to="/categories">Catégories</RouterLink>
                </li>
                <li>
                  <RouterLink to="/promotions">Promotions</RouterLink>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-lg-2 col-md-6 col-6">
            <div class="footer-column">
              <h4>Mon compte</h4>
              <ul>
                <li>
                  <RouterLink to="/connexion">Connexion</RouterLink>
                </li>
                <li>
                  <RouterLink to="/inscription">Inscription</RouterLink>
                </li>
                <li>
                  <RouterLink to="/profil">Mon profil</RouterLink>
                </li>
                <li>
                  <RouterLink to="/commandes">Mes commandes</RouterLink>
                </li>
              </ul>
            </div>
          </div>
          <div class="col-lg-4 col-md-6">
            <div class="footer-column">
              <h4>Besoin d'aide ?</h4>
              <div class="contact-item">
                <i class="bi bi-telephone"></i>
                <div>
                  <span>Appelez-nous</span>
                  <strong>+237 6XX XX XX XX</strong>
                </div>
              </div>
              <div class="contact-item">
                <i class="bi bi-envelope"></i>
                <div>
                  <span>Email</span>
                  <strong>contact@clever.com</strong>
                </div>
              </div>
              <div class="contact-item">
                <i class="bi bi-geo-alt"></i>
                <div>
                  <span>Localisation</span>
                  <strong>Cameroun</strong>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="footer-newsletter">
        <div>
          <h4>Recevez nos offres</h4>
          <p>
            Inscrivez-vous pour recevoir nos nouveautés et promotions.
          </p>
        </div>
        <form class="newsletter-form">
          <input
            type="email"
            placeholder="Votre adresse email"
          >
          <button type="submit">
            S'inscrire
          </button>
        </form>
      </div>
      <div class="footer-bottom">
        <span>
          © {{ new Date().getFullYear() }} CLEVER. Tous droits réservés.
        </span>
        <div>
          <RouterLink to="/conditions">
            Conditions générales
          </RouterLink>
          <RouterLink to="/confidentialite">
            Confidentialité
          </RouterLink>
          <RouterLink to="/livraison">
            Livraison
          </RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: #101828;
  color: #ffffff;
  margin-top: 70px;
  font-size: 13px;
}

.footer-top {
  padding: 45px 0 35px;
}

.footer-brand h3 {
  margin: 0 0 12px;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 1px;
}

.footer-brand p {
  max-width: 330px;
  margin: 0 0 18px;
  color: #98a2b3;
  font-size: 13px;
  line-height: 1.7;
}

.social-links {
  display: flex;
  gap: 8px;
}

.social-links a {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #1d2939;
  color: #98a2b3;
  text-decoration: none;
  font-size: 13px;
  transition: all 0.2s ease;
}

.social-links a:hover {
  background: #38b04c;
  color: #ffffff;
  transform: translateY(-2px);
}

.footer-column h4 {
  margin: 0 0 15px;
  font-size: 13px;
  font-weight: 700;
  color: #ffffff;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column li {
  margin-bottom: 9px;
}

.footer-column li a {
  color: #98a2b3;
  text-decoration: none;
  font-size: 12.5px;
  transition: color 0.2s ease;
}

.footer-column li a:hover {
  color: #38b04c;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 13px;
}

.contact-item > i {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1d2939;
  color: #38b04c;
  border-radius: 6px;
  font-size: 13px;
}

.contact-item div {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.contact-item span {
  color: #667085;
  font-size: 10px;
}

.contact-item strong {
  color: #d0d5dd;
  font-size: 12px;
  font-weight: 500;
}

.footer-newsletter {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 30px;
  padding: 22px 0;
  border-top: 1px solid #1d2939;
  border-bottom: 1px solid #1d2939;
}

.footer-newsletter h4 {
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 700;
}

.footer-newsletter p {
  margin: 0;
  color: #667085;
  font-size: 11px;
}

.newsletter-form {
  display: flex;
  width: 380px;
  max-width: 100%;
  height: 38px;
}

.newsletter-form input {
  flex: 1;
  min-width: 0;
  border: 1px solid #344054;
  border-right: none;
  background: #1d2939;
  color: #ffffff;
  outline: none;
  padding: 0 12px;
  font-size: 11px;
  border-radius: 5px 0 0 5px;
}

.newsletter-form input::placeholder {
  color: #667085;
}

.newsletter-form input:focus {
  border-color: #38b04c;
}

.newsletter-form button {
  border: none;
  padding: 0 16px;
  background: #38b04c;
  color: #ffffff;
  font-size: 11px;
  font-weight: 600;
  border-radius: 0 5px 5px 0;
  transition: background 0.2s ease;
}

.newsletter-form button:hover {
  background: #2f963f;
}

.footer-bottom {
  min-height: 55px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  color: #667085;
  font-size: 10.5px;
}

.footer-bottom > div {
  display: flex;
  gap: 18px;
}

.footer-bottom a {
  color: #667085;
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-bottom a:hover {
  color: #ffffff;
}

@media (max-width: 767px) {
  .footer {
    margin-top: 45px;
  }

  .footer-top {
    padding: 35px 0 25px;
  }

  .footer-newsletter {
    align-items: flex-start;
    flex-direction: column;
    gap: 15px;
  }

  .newsletter-form {
    width: 100%;
  }

  .footer-bottom {
    padding: 18px 0;
    flex-direction: column;
    justify-content: center;
    text-align: center;
  }

  .footer-bottom > div {
    justify-content: center;
    flex-wrap: wrap;
    gap: 12px;
  }
}
</style>