# MedStart website (Firebase results build)

## What's connected
- Firebase Email/Password authentication (sign up, sign in, sign out).
- Specialty quiz result saved in Firestore at `users/{uid}/results/quiz`.
- Latest medical-case score saved at `users/{uid}/results/case`.
- Home dashboard reads the signed-in user's results, including across devices.
- User-specific Firestore rules are included in `firestore.rules`.

## Before testing
1. In Firebase Console, open Authentication → Sign-in method and ensure **Email/Password** is enabled.
2. Open Firestore Database → Rules. Back up your existing rules, then copy the contents of `firestore.rules` into the Rules editor and click **Publish**. These rules preserve public reads of published article documents, keep article writes disabled, and restrict results to their owner. If your article publishing app needs admin writes later, implement a verified admin claim rather than opening writes to everyone.
3. In Authentication → Settings → Authorized domains, add your actual hosting domain (for example, your GitHub Pages domain or custom domain).
4. Upload the contents of this folder to your hosting provider with `index.html` at the root. Keep `firebase-config.js` beside the HTML files. The site needs internet access to load Firebase SDKs from Google's CDN.
5. Test by creating an account, completing the specialty quiz and a medical case, then return to Home. Sign in on another browser/device to verify results sync.

## Notes
- Client Firebase config is not a secret; Firestore rules and Authentication protect user data. Never put service-account credentials in this folder.
- Results are saved only when signed in. A result completed while signed out is displayed but not stored. Signing in after the fact does not retroactively save it; complete the activity again while signed in.
- This build stores the latest quiz result and latest case result, not a full history of every case.
- `firestore.rules` disables article writes for now because the article-admin publishing workflow is not yet implemented.
- For local testing, serve the folder through a local web server rather than relying on `file://`.


Design update: specialty discovery uses an original clean medical-education palette inspired by common editorial/medical learning layouts, not copied branding. Results show compatibility percentages and links to the specialty guide index. About credits Jesse Ogedengbe; Health Facts includes additional educational topics.


## Article links fix
- Article cards now open the included `article.html?id=...` page, which loads the selected published article from Firestore. This avoids broken links to generated `articles/<slug>.html` files. Upload `article.html` and the updated `articles.js` together with the rest of the site.


Individual article page added: `ebola-outbreak-2026-nigeria-confirms-case-as-virus-spreads-across-africa.html`. The Articles listing sends the exact title `Ebola Outbreak 2026: Nigeria Confirms Case as Virus Spreads Across Africa` to this page. The page loads the article's existing published content from Firestore, so its article record must exist and be published. Other article titles still use the generic article page until their own HTML files are added.
