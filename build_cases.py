import json, os, zipfile, re

specs = {
'General Surgery': [
 ('Acute appendicitis','A 10-year-old boy is brought to the emergency unit with 12 hours of worsening abdominal pain. The pain began around his umbilicus and moved to the right lower abdomen. He has fever, nausea and loss of appetite.','appendicitis'),
 ('Small-bowel obstruction','A 48-year-old woman comes with cramping abdominal pain, repeated vomiting, abdominal swelling and no passage of stool or gas. She had abdominal surgery several years ago.','obstruction'),
 ('Acute cholecystitis','A 42-year-old woman develops steady right-upper-quadrant pain and fever after several previous attacks of pain after meals. Ultrasound shows gallstones and a thickened gallbladder wall.','cholecystitis'),
 ('Incarcerated inguinal hernia','A 67-year-old man has a painful groin swelling that has become firm and cannot be pushed back. He now has vomiting and increasing abdominal pain.','hernia'),
 ('Blunt abdominal trauma','A 25-year-old man is brought after a road traffic crash. He is pale, sweaty and confused, with abdominal tenderness and a low blood pressure.','trauma'),
],
'Internal Medicine': [
 ('Diabetic ketoacidosis','A 19-year-old with diabetes arrives very thirsty and weak, passing urine frequently and vomiting. He is breathing deeply and his blood glucose is very high.','dka'),
 ('Acute decompensated heart failure','A 70-year-old man develops worsening breathlessness, cannot lie flat and has swollen legs. Examination suggests pulmonary congestion.','heartfailure'),
 ('Community-acquired pneumonia','A 56-year-old woman presents with fever, cough producing sputum, fast breathing and pleuritic chest pain. A chest X-ray shows a new focal infiltrate.','pneumonia'),
 ('Chronic kidney disease','A 61-year-old man with long-standing hypertension and diabetes has persistent proteinuria and gradually worsening kidney function.','ckd'),
 ('Iron-deficiency anaemia','A 34-year-old woman reports tiredness, dizziness and reduced exercise tolerance. Blood tests show low haemoglobin with small, pale red cells.','anaemia'),
],
'Pediatrics': [
 ('Childhood malaria','A 7-year-old boy from an area where malaria is common presents with high fever, chills, headache and weakness. He is drowsy but can be roused.','malaria'),
 ('Neonatal jaundice','A 3-day-old newborn develops yellow discoloration of the eyes and skin. The baby is feeding less well than before.','jaundice'),
 ('Acute asthma in a child','A 9-year-old girl with previous episodes of wheezing develops cough, chest tightness and difficulty breathing after a dusty day.','asthma'),
 ('Acute gastroenteritis with dehydration','A 2-year-old boy has had frequent watery stools and vomiting since yesterday. He is thirsty and has fewer wet diapers.','dehydration'),
 ('Sickle-cell pain crisis','A 12-year-old with known sickle-cell disease presents with severe limb and back pain after several days of poor fluid intake.','sickle'),
],
'Obstetrics & Gynecology': [
 ('Ectopic pregnancy','A 24-year-old woman with a missed period develops one-sided lower abdominal pain, vaginal bleeding and dizziness. A pregnancy test is positive.','ectopic'),
 ('Postpartum haemorrhage','A woman gives birth vaginally and soon develops heavy vaginal bleeding. Her uterus feels soft and enlarged.','pph'),
 ('Severe pre-eclampsia','A 30-year-old woman at 35 weeks has severe headache, visual symptoms and high blood pressure. Urine testing shows significant protein.','preeclampsia'),
 ('Obstructed labour','A woman in labour has been pushing for hours with poor progress. The fetal head remains high and there are signs of maternal exhaustion.','obstructed'),
 ('Ovarian torsion','A 17-year-old girl develops sudden severe one-sided lower abdominal pain with vomiting. Examination shows marked tenderness.','torsion'),
],
'Emergency Medicine': [
 ('Road-traffic polytrauma','A 22-year-old man is brought after a road traffic crash. He has severe bleeding from a leg wound and is becoming confused and pale.','polytrauma'),
 ('Acute severe asthma','A 20-year-old with asthma arrives unable to complete full sentences because of breathlessness. He is using accessory muscles to breathe.','severeasthma'),
 ('Anaphylaxis','A 16-year-old develops sudden wheezing, facial swelling and dizziness minutes after eating a food he has reacted to before.','anaphylaxis'),
 ('Acute stroke','A 68-year-old woman suddenly develops facial drooping, arm weakness and difficulty speaking. Symptoms began less than an hour ago.','stroke'),
 ('Sepsis','A 64-year-old man with a suspected infection is confused, breathing rapidly and has low blood pressure.','sepsis'),
],
'Cardiology': [
 ('Acute myocardial infarction','A 58-year-old man develops crushing central chest pain with sweating and nausea. An ECG shows acute ST-segment elevation in contiguous leads.','mi'),
 ('Acute heart failure','A 72-year-old woman presents with severe breathlessness, orthopnoea and crackles in both lungs. Her legs are swollen.','chf'),
 ('Atrial fibrillation','A 66-year-old man reports palpitations and fatigue. His pulse is irregularly irregular.','af'),
 ('Infective endocarditis','A 35-year-old with a history of intravenous drug use has fever, weight loss and a new heart murmur.','endocarditis'),
 ('Hypertensive emergency','A 54-year-old patient has very high blood pressure with severe headache and new neurological symptoms.','hypertensive'),
],
'Orthopedic Surgery': [
 ('Femoral shaft fracture','A 28-year-old man is brought after a high-speed crash with severe thigh pain and an obviously deformed leg.','femur'),
 ('Hip fracture in an older adult','A 78-year-old woman falls at home and develops severe hip pain. She cannot stand and the affected leg appears shortened and rotated.','hip'),
 ('Septic arthritis','A 9-year-old boy develops fever and severe pain in his knee. He refuses to walk and the joint is swollen.','septicjoint'),
 ('Acute compartment syndrome','A young man develops increasing severe pain and tight swelling in his lower leg several hours after a fracture.','compartment'),
 ('ACL injury','A 21-year-old football player twists his knee while changing direction and hears a pop. The knee later feels unstable.','acl'),
],
'Anesthesiology': [
 ('Pre-operative assessment','A 62-year-old man is booked for major abdominal surgery. He has hypertension and diabetes and takes several medicines.','preop'),
 ('Difficult airway','A patient requires urgent surgery and examination suggests limited mouth opening and a difficult airway.','airway'),
 ('Spinal anaesthesia','A 45-year-old woman receives spinal anaesthesia for lower-limb surgery and soon becomes hypotensive.','spinal'),
 ('Post-operative pain','A patient reports significant pain after major surgery despite receiving a single analgesic.','pain'),
 ('Malignant hyperthermia','During general anaesthesia, a young patient develops rapidly rising temperature, muscle rigidity and increasing carbon dioxide levels.','mh'),
],
'Neurology': [
 ('Acute ischemic stroke','A 71-year-old man suddenly develops right-sided weakness and difficulty speaking while eating breakfast.','neurostroke'),
 ('Generalized seizure','A 16-year-old has a witnessed episode of loss of consciousness followed by rhythmic jerking and confusion afterward.','seizure'),
 ('Meningitis','A 19-year-old presents with fever, severe headache, neck stiffness and photophobia.','meningitis'),
 ('Parkinson disease','A 67-year-old develops a resting tremor, slowness of movement and muscle rigidity over several months.','parkinson'),
 ('Migraine','A 23-year-old woman has recurrent throbbing headaches with nausea and sensitivity to light.','migraine'),
],
'Radiology': [
 ('Chest X-ray in pneumonia','A 45-year-old has fever, cough and shortness of breath. A chest X-ray is requested to assess the lungs.','cxr'),
 ('CT in trauma','A patient with significant trauma is stable enough for imaging but has concern for internal injury.','cttrauma'),
 ('MRI brain','A patient has neurological symptoms requiring detailed assessment of brain soft tissue.','mri'),
 ('Obstetric ultrasound','A pregnant woman attends for fetal assessment and dating.','ob ultrasound'),
 ('Image-guided biopsy','A patient has a suspicious mass and needs tissue obtained accurately with imaging guidance.','biopsy'),
],
}

# Specialty-specific question sets. Each case gets 5 questions tied to the scenario.
Q = {
'General Surgery': [
 [('Most likely diagnosis?',['Acute appendicitis','Acute pancreatitis','Renal colic','Peptic ulcer disease']),0],
 [('Which initial assessment is most important in a sick surgical patient?',['Airway, breathing, circulation and vital signs','Only the patient’s diet history','Only the family history','Only the pain score']),0],
 [('Which investigation is commonly used to support the diagnosis in this scenario?',['Abdominal ultrasound or CT when appropriate','Electroencephalogram','Echocardiogram only','Bone-density scan']),0],
 [('Which complication would make the situation more urgent?',['Perforation or generalized peritonitis','Mild thirst','Stable appetite','Simple headache']),0],
 [('What is the key role of the surgeon?',['Assess for and provide operative management when indicated','Only prescribe glasses','Only interpret ECGs','Only manage skin disease']),0],
],
'Internal Medicine': [
 [('What is the main problem described?',['A serious adult medical condition requiring assessment and treatment','An isolated skin lesion','A dental emergency','A simple eye refractive error']),0],
 [('Which first principle is important in an acutely unwell adult?',['Assess severity, stabilize and identify the cause','Delay all assessment for a week','Treat symptoms without examination','Ignore vital signs']),0],
 [('Which type of test is commonly relevant to this case?',['Blood tests and targeted imaging or monitoring','Only a hearing test','Only a skin biopsy','Only an eye examination']),0],
 [('Which complication should clinicians actively watch for?',['Organ dysfunction or clinical deterioration','Improved appetite','Normal hydration','Stable vital signs']),0],
 [('What is a key role of internal medicine?',['Managing complex non-operative adult disease and coordinating care','Performing every operation','Providing only dental treatment','Fitting hearing aids']),0],
],
'Pediatrics': [
 [('What is the most important first step in this child?',['Assess severity and immediate danger signs','Assume the child is fine','Ignore hydration','Wait several weeks']),0],
 [('Which factor is especially important in children?',['Age, weight and developmental stage','Only shoe size','Only occupation','Only adult BMI categories']),0],
 [('Which assessment is commonly useful?',['Age-appropriate examination and targeted tests','Only an adult treadmill test','Only a bone-density scan','Only a colonoscopy']),0],
 [('Which complication should be watched for?',['Rapid deterioration or dehydration/organ complications','Improved appetite','Normal play','Stable breathing']),0],
 [('What is the pediatrician’s role?',['Manage childhood illness and coordinate specialist care when needed','Treat only adults','Perform all orthopedic operations','Interpret every X-ray exclusively']),0],
],
'Obstetrics & Gynecology': [
 [('What is the most likely clinical problem?',['A potentially urgent obstetric or gynecologic condition','Simple seasonal allergy','Dental caries','Chronic earwax']),0],
 [('What should be assessed first in an unstable patient?',['Airway, breathing, circulation and vital signs','Only the menstrual calendar','Only family history','Only body weight']),0],
 [('Which investigation is commonly important?',['Pregnancy testing and targeted ultrasound when appropriate','Only an EEG','Only a hearing test','Only a bone scan']),0],
 [('Which complication can be life-threatening?',['Major bleeding, shock or organ complications','Mild acne','Temporary hunger','Normal fetal movement']),0],
 [('What does the specialty cover?',['Pregnancy, childbirth and diseases of the female reproductive system','Only childhood infections','Only fractures','Only lung imaging']),0],
],
'Emergency Medicine': [
 [('What is the immediate priority?',['Rapid ABC assessment, stabilization and identification of life threats','Complete a long outpatient questionnaire first','Wait for symptoms to disappear','Only check temperature']),0],
 [('Which finding would increase urgency?',['Shock, severe breathing difficulty or altered consciousness','Normal vital signs','Mild hunger','A healed old scar']),0],
 [('What type of investigation may be needed urgently?',['Focused bedside tests and targeted imaging/laboratory tests','Only a routine eye test','Only a dental X-ray','Only a hearing test']),0],
 [('Why is reassessment important?',['A patient can deteriorate quickly and treatment response must be checked','It is never needed','Only for paperwork','Only after discharge']),0],
 [('What is a core emergency-medicine role?',['Stabilize undifferentiated acute illness and arrange definitive care','Provide only long-term prescriptions','Perform only elective surgery','Only interpret pathology slides']),0],
],
'Cardiology': [
 [('What is the most likely cardiac problem?',['A cardiovascular condition requiring focused assessment','A primary skin disorder','A dental infection','An isolated eye problem']),0],
 [('Which bedside assessment is particularly important?',['Pulse, blood pressure, heart sounds and signs of congestion/perfusion','Only visual acuity','Only abdominal girth','Only hearing']),0],
 [('Which test is commonly central?',['ECG and/or echocardiography depending on the case','Only a skin swab','Only a urine pregnancy test','Only a bone scan']),0],
 [('Which complication can be dangerous?',['Arrhythmia, shock or worsening heart failure','Mild dry skin','Simple hunger','Normal sleep']),0],
 [('What does a cardiologist mainly manage?',['Diseases of the heart and cardiovascular system','Only fractures','Only pregnancy','Only skin disease']),0],
],
'Orthopedic Surgery': [
 [('What is the main problem?',['A musculoskeletal injury or disease','A primary lung infection','A dental condition','A simple eye problem']),0],
 [('What should be checked early?',['Neurovascular status, pain and function of the affected limb','Only appetite','Only hearing','Only blood group']),0],
 [('Which investigation is commonly relevant?',['X-ray and other imaging when indicated','Only EEG','Only spirometry','Only an ECG in every case']),0],
 [('Which complication is important to detect?',['Neurovascular compromise, infection or compartment syndrome when relevant','Mild thirst','Normal mobility','Simple headache']),0],
 [('What does orthopedic surgery focus on?',['Bones, joints, muscles, ligaments and related musculoskeletal problems','Only the heart','Only pregnancy','Only skin conditions']),0],
],
'Anesthesiology': [
 [('What is the key anesthetic concern?',['Safe peri-operative control of airway, breathing, circulation, pain and consciousness','Only the patient’s height','Only the family tree','Only skin appearance']),0],
 [('What should be assessed before anesthesia?',['Medical history, medicines, airway and peri-operative risk','Only favorite food','Only occupation','Only eye color']),0],
 [('Which monitoring is important during anesthesia?',['Oxygenation, ventilation, circulation and depth of anesthesia','Only body weight once','Only hearing','Only skin temperature once']),0],
 [('Which complication can become rapidly life-threatening?',['Airway failure, severe hypotension or major anesthetic reaction','Mild hunger','Normal sleep','A healed scar']),0],
 [('What is a core role of anesthesiology?',['Providing safe anesthesia, resuscitation, peri-operative and often critical-care support','Only interpreting X-rays','Only treating fractures','Only prescribing antibiotics']),0],
],
'Neurology': [
 [('What is the main system involved?',['Brain, spinal cord, peripheral nerves or related neurological function','Only the skin','Only the teeth','Only the gallbladder']),0],
 [('What neurological feature is especially important?',['Time of onset and pattern of neurological deficits','Only appetite','Only shoe size','Only skin color']),0],
 [('Which test may be important depending on the case?',['Brain imaging, EEG or lumbar puncture when indicated','Only bone-density testing','Only dental X-ray','Only visual acuity']),0],
 [('Which complication requires urgent attention?',['Reduced consciousness, airway compromise or worsening neurological deficit','Mild thirst','Normal sleep','Stable chronic symptoms']),0],
 [('What does neurology mainly manage?',['Disorders of the nervous system','Only surgical wounds','Only pregnancy','Only kidney stones']),0],
],
'Radiology': [
 [('What is the radiologist’s main task in this case?',['Select or interpret appropriate diagnostic imaging and communicate important findings','Perform all bedside examinations','Prescribe every medicine','Provide physiotherapy']),0],
 [('Which imaging modality fits the scenario?',['The modality described in the case and appropriate to the clinical question','Always an MRI regardless of the problem','Always an X-ray regardless of the problem','No imaging can ever be useful']),0],
 [('What is important before imaging?',['The clinical question, patient safety and relevant contraindications','Only the patient’s favorite food','Only shoe size','Only family occupation']),0],
 [('What makes a radiology finding urgent?',['A finding that suggests an immediate threat to life or organ function','A normal scan','A healed old injury','A routine stable finding']),0],
 [('What is interventional radiology?',['Using imaging guidance for minimally invasive procedures','Reading only blood tests','Treating only skin diseases','Performing only open abdominal surgery']),0],
]
}

# Case-specific overrides for diagnosis/first question and a few case facts.
first_correct = {
 'appendicitis':'Acute appendicitis','obstruction':'Small-bowel obstruction','cholecystitis':'Acute cholecystitis','hernia':'Incarcerated/strangulated hernia','trauma':'Intra-abdominal bleeding/hemorrhagic shock',
 'dka':'Diabetic ketoacidosis','heartfailure':'Acute decompensated heart failure','pneumonia':'Community-acquired pneumonia','ckd':'Chronic kidney disease','anaemia':'Iron-deficiency anaemia',
 'malaria':'Malaria','jaundice':'Neonatal jaundice requiring assessment','asthma':'Acute asthma exacerbation','dehydration':'Acute gastroenteritis with dehydration','sickle':'Sickle-cell pain crisis',
 'ectopic':'Ectopic pregnancy','pph':'Postpartum haemorrhage','preeclampsia':'Severe pre-eclampsia','obstructed':'Obstructed labour','torsion':'Ovarian torsion',
 'polytrauma':'Traumatic shock/polytrauma','severeasthma':'Acute severe asthma','anaphylaxis':'Anaphylaxis','stroke':'Acute stroke','sepsis':'Sepsis with shock risk',
 'mi':'Acute myocardial infarction','chf':'Acute decompensated heart failure','af':'Atrial fibrillation','endocarditis':'Infective endocarditis','hypertensive':'Hypertensive emergency',
 'femur':'Femoral shaft fracture','hip':'Hip fracture','septicjoint':'Septic arthritis','compartment':'Acute compartment syndrome','acl':'Anterior cruciate ligament injury',
 'preop':'Peri-operative risk assessment','airway':'Difficult airway','spinal':'Hypotension after spinal anaesthesia','pain':'Post-operative pain','mh':'Malignant hyperthermia',
 'neurostroke':'Acute ischemic stroke','seizure':'Generalized seizure','meningitis':'Meningitis','parkinson':'Parkinson disease','migraine':'Migraine',
 'cxr':'Pneumonia assessment on chest X-ray','cttrauma':'CT assessment for traumatic injury','mri':'MRI brain assessment','ob ultrasound':'Obstetric ultrasound assessment','biopsy':'Image-guided biopsy'
}

def build_questions(spec, tag, case_index):
    base=Q[spec]
    out=[]
    for qi,item in enumerate(base):
        (q,opts),ci=item
        opts=list(opts); idx=ci
        if qi==0:
            correct=first_correct[tag]
            # replace option A with specific correct, keeping plausible options from original
            old=opts[0]; opts[0]=correct
        # Make question 1 explicitly case-specific
        if qi==0:
            q='Based on the history, what is the most likely diagnosis or main clinical problem?'
        elif qi==1:
            q='Which is the most important next clinical step in this patient?'
        elif qi==2:
            q='Which investigation or assessment would be most useful for this patient?'
        elif qi==3:
            q='Which complication or danger should the team be especially alert for?'
        elif qi==4:
            q='Which statement best describes the specialist’s role in this case?'
        # Customize correct answers for question 2-5 by tag where useful
        custom = {
         'appendicitis': ['Acute appendicitis','Assess ABCs, examine and obtain appropriate surgical investigations','Abdominal ultrasound or CT when appropriate','Perforation/peritonitis','Surgical assessment and appendicectomy when indicated'],
         'obstruction':['Small-bowel obstruction','Resuscitate, correct fluids/electrolytes and obtain urgent surgical assessment','Abdominal imaging such as CT when appropriate','Strangulation, ischemia or perforation','Surgical management when obstruction is complicated or does not resolve'],
         'cholecystitis':['Acute cholecystitis','Assess severity, provide supportive treatment and surgical review','Ultrasound of the gallbladder','Sepsis or gallbladder perforation','Definitive gallbladder surgery when indicated'],
         'hernia':['Incarcerated/strangulated hernia','Resuscitate and obtain urgent surgical review','Clinical examination with imaging when diagnosis is uncertain','Bowel ischemia/necrosis','Urgent reduction or surgery depending on findings'],
         'trauma':['Intra-abdominal bleeding/hemorrhagic shock','Rapid trauma assessment with simultaneous resuscitation','Focused ultrasound/CT depending on stability','Ongoing hemorrhagic shock','Control bleeding and coordinate definitive trauma surgery'],
        }
        if tag in custom and qi>0:
            opts[0]=custom[tag][qi]
        out.append({'question':q,'options':opts,'correct':0,'explanation':f'This is the key learning point for this case: {opts[0]}.'})
    return out

BANK={}
for spec,cases in specs.items():
    BANK[spec]=[]
    for i,(title,stem,tag) in enumerate(cases):
        qs=build_questions(spec,tag,i)
        BANK[spec].append({'title':title,'stem':stem,'questions':qs})

# Specialize some correct answers for all specialties by changing the first option already done; for the remaining generic questions,
# keep clinically broad but useful. This is an educational prototype, not a diagnostic tool.

html_path='/mnt/data/case_edit/cases.html'
html=open(html_path,encoding='utf-8').read()
start=html.index('<script>\nconst BANK=')
end=html.index('</script>',start)
# Preserve first script opening and replace entire app script body.
script='''<script>\nconst BANK='''+json.dumps(BANK,ensure_ascii=False,separators=(',',':'))+''';
const names=Object.keys(BANK);let specialty=names[0],caseIndex=0,qIndex=0,caseAnswers=Array.from({length:5},()=>Array(5).fill(undefined));const tabs=document.getElementById('tabs'),app=document.getElementById('app');
function optionOrder(q){const a=q.options.map((_,i)=>i);let seed=(q.question.length*31+q.options[0].length*17+q.options[1].length*13)%997;for(let i=a.length-1;i>0;i--){seed=(seed*73+41)%1009;const j=seed%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function slug(x){return x.toLowerCase().replace(/[^a-z0-9]+/g,'-')}
function getSigned(){try{return localStorage.getItem('medstartSignedIn')==='true'}catch(e){return false}}
function renderTabs(){tabs.innerHTML=names.map(n=>`<button class="tab ${n===specialty?'active':''}" data-s="${slug(n)}">${n}</button>`).join('');tabs.querySelectorAll('.tab').forEach(b=>b.onclick=()=>{specialty=names.find(n=>slug(n)===b.dataset.s);caseIndex=0;qIndex=0;caseAnswers=Array.from({length:5},()=>Array(5).fill(undefined));render()})}
function render(){renderTabs();const c=BANK[specialty][caseIndex],q=c.questions[qIndex],chosen=caseAnswers[caseIndex][qIndex],order=optionOrder(q);app.innerHTML=`<div class="case-card"><div class="case-num">CASE ${caseIndex+1} OF 5 · QUESTION ${qIndex+1} OF 5 · ${specialty.toUpperCase()}</div><h2 class="case-title">${c.title}</h2><p class="stem"><strong>Case:</strong> ${c.stem}</p><div class="question-box"><p class="stem"><strong>Question ${qIndex+1}:</strong> ${q.question}</p><div class="options">${q.options.map((o,i)=>`<button class="opt ${chosen===i?'selected':''}" data-i="${i}">${String.fromCharCode(65+i)}. ${o}</button>`).join('')}</div></div><div class="progress"><i style="width:${((qIndex+1)/5)*100}%"></i></div><div class="controls"><button class="action secondary" id="prev" ${qIndex===0?'disabled':''}>← Previous question</button><button class="action" id="next">${qIndex===4?(caseIndex===4?'Finish specialty':'Next case →'):'Next question →'}</button></div></div>`;app.querySelectorAll('.opt').forEach(b=>b.onclick=()=>{caseAnswers[caseIndex][qIndex]=Number(b.dataset.i);render()});document.getElementById('prev').onclick=()=>{if(qIndex>0){qIndex--;render()}};document.getElementById('next').onclick=()=>{if(caseAnswers[caseIndex][qIndex]===undefined){alert('Choose an answer to continue.');return}if(qIndex<4){qIndex++;render()}else if(caseIndex<4){caseIndex++;qIndex=0;render()}else{finishSpecialty()}}}
function saveResult(score){let all={};try{all=JSON.parse(localStorage.getItem('medstartCaseResults')||'{}')}catch(e){}all[specialty]={specialty,total:25,score,completedCases:5,updatedAt:new Date().toISOString()};localStorage.setItem('medstartCaseResults',JSON.stringify(all))}
function finishSpecialty(){let score=0;const reviews=[];for(let ci=0;ci<5;ci++){const ca=BANK[specialty][ci];let cs=0;for(let qi=0;qi<5;qi++){const a=caseAnswers[ci][qi];if(a!==undefined && a===ca.questions[qi].correct)cs++;}score+=cs;reviews.push({title:ca.title,score:cs,questions:ca.questions,answers:caseAnswers[ci]});}saveResult(score);app.innerHTML=`<div class="result"><div class="eyebrow">${specialty.toUpperCase()} · 5 CASES COMPLETE</div><div class="score">${score}/25</div><h2>Specialty case result</h2><p class="note">Your score is saved on this device. If you are signed in, it will appear on your MedStart dashboard. If you complete another specialty, its result will be saved separately too.</p>${reviews.map((r,i)=>`<div class="review"><strong>Case ${i+1}: ${r.title}</strong><div class="correct">${r.score}/5 questions correct</div></div>`).join('')}<div class="controls"><button class="action secondary" id="again">Retry ${specialty}</button><button class="action" id="nextSpec">Next specialty →</button></div></div>`;document.getElementById('again').onclick=()=>{caseIndex=0;qIndex=0;caseAnswers=Array.from({length:5},()=>Array(5).fill(undefined));render()};document.getElementById('nextSpec').onclick=()=>{specialty=names[(names.indexOf(specialty)+1)%names.length];caseIndex=0;qIndex=0;caseAnswers=Array.from({length:5},()=>Array(5).fill(undefined));render()}}
render();document.getElementById('navNext').onclick=()=>document.getElementById('nav').scrollBy({left:280,behavior:'smooth'});
</script>'''
html=html[:start]+script+html[end+9:]
# update hero copy
html=html.replace('50 educational cases across 10 major specialties. Each specialty has five cases. Choose an answer, learn why it fits, and track your score.','50 clinical cases across 10 major specialties. Each specialty has five cases, and each case has five important questions. Complete all five cases in a specialty to receive a score out of 25.')
# Add a note about sign-in behavior
html=html.replace('<div class="tabs" id="tabs"></div><div id="app"></div>','<div class="tabs" id="tabs"></div><div class="note" style="margin:0 0 12px">Complete all 5 cases in a specialty for a 25-question specialty score. Sign in to have your completed specialty scores appear on your dashboard.</div><div id="app"></div>')
open(html_path,'w',encoding='utf-8').write(html)

# Fix dashboard to display per-specialty case results clearly, only when signed in.
idx='/mnt/data/case_edit/index.html'; h=open(idx,encoding='utf-8').read()
old="""if(entries.length){const latest=entries.slice(-10).reverse();cbox.innerHTML=latest.map((r,i)=>{const title=r.title||r.case||('Clinical Case '+(i+1));const score=Number(r.score);const total=Number(r.total||5);const label=Number.isFinite(score)?Math.max(0,Math.min(total,score))+'/'+total:'Completed';return '<div class=\"personal-result\"><strong>'+title+'</strong><small>'+label+(r.updatedAt?' · '+new Date(r.updatedAt).toLocaleDateString():'')+'</small></div>'}).join('');}"""
new="""if(entries.length){const latest=entries.slice().reverse();cbox.innerHTML=latest.map((r)=>{const title=r.specialty||r.title||r.case||'Clinical Case';const score=Number(r.score);const total=Number(r.total||25);const pct=total?Math.round((score/total)*100):0;return '<a class=\"personal-result\" href=\"cases.html\"><strong>'+title+'</strong><div class=\"mini-bar\"><i style=\"width:'+pct+'%\"></i></div><small>'+score+'/'+total+' questions correct · '+pct+'%'+(r.updatedAt?' · '+new Date(r.updatedAt).toLocaleDateString():'')+'</small></a>';}).join('');}"""
if old not in h: print('dashboard old block not found')
else: h=h.replace(old,new)
open(idx,'w',encoding='utf-8').write(h)

# Update notes
notes='/mnt/data/case_edit/CASES_NOTES.txt'
open(notes,'a',encoding='utf-8').write('\n\nUPDATED CASE FORMAT\nEach of the 10 specialties has 5 cases. Each case contains 5 questions, for 25 questions per specialty. Completing all 5 cases saves a specialty result to localStorage under medstartCaseResults as score/25. The home dashboard shows every completed specialty case result only after sign-in. Completing all 10 specialties produces 10 separate dashboard entries.\n')

out='/mnt/data/MedStart_CASES_5Q_EACH_DASHBOARD.zip'
with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED) as z:
    for root,dirs,files in os.walk('/mnt/data/case_edit'):
        for f in files:
            p=os.path.join(root,f); z.write(p,os.path.relpath(p,'/mnt/data/case_edit'))
print(out, os.path.getsize(out))
print('cases',sum(len(v) for v in BANK.values()),'questions',sum(len(c['questions']) for v in BANK.values() for c in v))
