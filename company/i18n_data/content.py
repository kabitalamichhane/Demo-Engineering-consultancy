"""Nepali and Hindi for the long paragraphs and the starter content created by `seed_demo_data`
(services, statistics, chatbot questions) plus project / job / news labels."""
from company.director_defaults import DEFAULT_MESSAGE, DEFAULT_TITLE

DATA = {
    # ---- long paragraphs on the pages
    'Highnoon Engineering Solutions Pvt. Ltd. is an engineering, construction and metal fabrication company based in Pokhara, Nepal. We work across engineering consultancy, building construction, infrastructure and structural works, with metal fabrication as a core part of what we do — from steel structures and frames to gates, railings and staircases built to specification.': (
        'हाइनुन इन्जिनियरिङ सोलुसन्स प्रा. लि. पोखरा, नेपालमा आधारित इन्जिनियरिङ, निर्माण र धातु फ्याब्रिकेसन कम्पनी हो। हामी इन्जिनियरिङ परामर्श, भवन निर्माण, पूर्वाधार र संरचनात्मक कार्यमा काम गर्छौं, जसमा धातु फ्याब्रिकेसन हाम्रो कामको मुख्य हिस्सा हो — स्टिल संरचना र फ्रेमदेखि विनिर्देश अनुसार बनाइएका गेट, रेलिङ र भ्र्याङसम्म।',
        'हाईनून इंजीनियरिंग सॉल्यूशंस प्रा. लि. पोखरा, नेपाल स्थित इंजीनियरिंग, निर्माण और धातु फैब्रिकेशन कंपनी है। हम इंजीनियरिंग परामर्श, भवन निर्माण, बुनियादी ढाँचा और संरचनात्मक कार्यों में काम करते हैं, जिसमें धातु फैब्रिकेशन हमारे काम का एक प्रमुख हिस्सा है — स्टील संरचनाओं और फ्रेम से लेकर विनिर्देश के अनुसार बने गेट, रेलिंग और सीढ़ियों तक।'),
    'provides engineering, construction and metal fabrication services from Pokhara, Nepal. Our work spans engineering consultancy, structural engineering, building construction, infrastructure development and custom fabrication.': (
        'पोखरा, नेपालबाट इन्जिनियरिङ, निर्माण र धातु फ्याब्रिकेसन सेवा प्रदान गर्छ। हाम्रो काम इन्जिनियरिङ परामर्श, संरचनात्मक इन्जिनियरिङ, भवन निर्माण, पूर्वाधार विकास र अनुकूलित फ्याब्रिकेसनसम्म फैलिएको छ।',
        'पोखरा, नेपाल से इंजीनियरिंग, निर्माण और धातु फैब्रिकेशन सेवाएँ प्रदान करती है। हमारा काम इंजीनियरिंग परामर्श, संरचनात्मक इंजीनियरिंग, भवन निर्माण, बुनियादी ढाँचा विकास और कस्टम फैब्रिकेशन तक फैला है।'),
    'Our approach combines careful engineering, practical construction methods and custom fabrication, so that every project — residential, commercial, industrial or institutional — is handled with attention to quality and safety from planning through to completion.': (
        'हाम्रो दृष्टिकोणले सावधानीपूर्वक इन्जिनियरिङ, व्यावहारिक निर्माण विधि र अनुकूलित फ्याब्रिकेसनलाई जोड्छ, ताकि प्रत्येक परियोजना — आवासीय, व्यावसायिक, औद्योगिक वा संस्थागत — योजनादेखि सम्पन्न हुँदासम्म गुणस्तर र सुरक्षामा ध्यान दिएर सञ्चालन गरियोस्।',
        'हमारा दृष्टिकोण सावधानीपूर्ण इंजीनियरिंग, व्यावहारिक निर्माण विधियों और कस्टम फैब्रिकेशन को जोड़ता है, ताकि हर परियोजना — आवासीय, वाणिज्यिक, औद्योगिक या संस्थागत — योजना से लेकर पूर्णता तक गुणवत्ता और सुरक्षा पर ध्यान देकर संभाली जाए।'),
    'We approach every project — from structural works to steel and metal fabrication — with a focus on sound engineering practice, coordinated execution and clear communication with clients, contractors and partners.': (
        'संरचनात्मक कार्यदेखि स्टिल र धातु फ्याब्रिकेसनसम्म, हामी प्रत्येक परियोजनामा सुदृढ इन्जिनियरिङ अभ्यास, समन्वित कार्यान्वयन र ग्राहक, ठेकेदार तथा साझेदारहरूसँग स्पष्ट सञ्चारमा ध्यान दिन्छौं।',
        'संरचनात्मक कार्यों से लेकर स्टील और धातु फैब्रिकेशन तक, हम हर परियोजना में मजबूत इंजीनियरिंग पद्धति, समन्वित क्रियान्वयन और ग्राहकों, ठेकेदारों तथा साझेदारों के साथ स्पष्ट संवाद पर ध्यान देते हैं।'),
    'Metal fabrication is a major part of what we do. We work on custom metal fabrication, structural steel fabrication, steel frames, gates, railings, staircases and industrial fabrication — built according to drawings and specifications, with installation support where applicable.': (
        'धातु फ्याब्रिकेसन हाम्रो कामको ठूलो हिस्सा हो। हामी अनुकूलित धातु फ्याब्रिकेसन, संरचनात्मक स्टिल फ्याब्रिकेसन, स्टिल फ्रेम, गेट, रेलिङ, भ्र्याङ र औद्योगिक फ्याब्रिकेसनमा काम गर्छौं — नक्सा र विनिर्देश अनुसार बनाइएको, आवश्यक परे जडान सहयोगसहित।',
        'धातु फैब्रिकेशन हमारे काम का एक बड़ा हिस्सा है। हम कस्टम धातु फैब्रिकेशन, संरचनात्मक स्टील फैब्रिकेशन, स्टील फ्रेम, गेट, रेलिंग, सीढ़ियों और औद्योगिक फैब्रिकेशन पर काम करते हैं — ड्रॉइंग और विनिर्देशों के अनुसार बने, जहाँ लागू हो वहाँ स्थापना सहयोग के साथ।'),
    'As a metal fabrication company in Pokhara, Nepal, Highnoon Engineering Solutions works on custom metal fabrication and structural steel fabrication for engineering, construction and industrial projects. Our fabrication work is carried out according to drawings and specifications, with installation support provided where applicable.': (
        'पोखरा, नेपालको धातु फ्याब्रिकेसन कम्पनीका रूपमा हाइनुन इन्जिनियरिङ सोलुसन्सले इन्जिनियरिङ, निर्माण र औद्योगिक परियोजनाका लागि अनुकूलित धातु फ्याब्रिकेसन र संरचनात्मक स्टिल फ्याब्रिकेसनमा काम गर्छ। हाम्रो फ्याब्रिकेसन कार्य नक्सा र विनिर्देश अनुसार गरिन्छ, आवश्यक परे जडान सहयोग उपलब्ध गराइन्छ।',
        'पोखरा, नेपाल की धातु फैब्रिकेशन कंपनी के रूप में हाईनून इंजीनियरिंग सॉल्यूशंस इंजीनियरिंग, निर्माण और औद्योगिक परियोजनाओं के लिए कस्टम धातु फैब्रिकेशन और संरचनात्मक स्टील फैब्रिकेशन पर काम करती है। हमारा फैब्रिकेशन कार्य ड्रॉइंग और विनिर्देशों के अनुसार किया जाता है, जहाँ लागू हो वहाँ स्थापना सहयोग दिया जाता है।'),
    'From structural frames to perforated facade screens, fabricated metal shapes how a building looks and performs. Explore what custom metal fabrication and engineering can do for your project in Pokhara and across Nepal.': (
        'संरचनात्मक फ्रेमदेखि छिद्रित अगाडिको भागका पर्दासम्म, फ्याब्रिकेसन गरिएको धातुले भवन कस्तो देखिन्छ र कस्तो काम गर्छ भन्ने निर्धारण गर्छ। पोखरा र सम्पूर्ण नेपालमा तपाईंको परियोजनाका लागि अनुकूलित धातु फ्याब्रिकेसन र इन्जिनियरिङले के गर्न सक्छ, हेर्नुहोस्।',
        'संरचनात्मक फ्रेम से लेकर छिद्रित अग्रभाग की स्क्रीन तक, फैब्रिकेटेड धातु तय करती है कि इमारत कैसी दिखती है और कैसा प्रदर्शन करती है। पोखरा और पूरे नेपाल में आपकी परियोजना के लिए कस्टम धातु फैब्रिकेशन और इंजीनियरिंग क्या कर सकती है, देखें।'),
    'Steel fabrication and industrial metal fabrication form a core part of our engineering and construction services in Nepal, supporting both new builds and renovation work.': (
        'स्टिल फ्याब्रिकेसन र औद्योगिक धातु फ्याब्रिकेसन नेपालमा हाम्रा इन्जिनियरिङ र निर्माण सेवाको मुख्य हिस्सा हुन्, जसले नयाँ निर्माण र नवीकरण दुवै कार्यलाई सहयोग गर्छ।',
        'स्टील फैब्रिकेशन और औद्योगिक धातु फैब्रिकेशन नेपाल में हमारी इंजीनियरिंग और निर्माण सेवाओं का मुख्य हिस्सा हैं, जो नए निर्माण और नवीनीकरण दोनों कार्यों में सहायक हैं।'),
    'Engineering, construction and metal fabrication solutions delivered with a commitment to quality, safety and reliability.': (
        'गुणस्तर, सुरक्षा र भरोसायोग्यताप्रतिको प्रतिबद्धतासहित उपलब्ध गराइने इन्जिनियरिङ, निर्माण र धातु फ्याब्रिकेसन समाधान।',
        'गुणवत्ता, सुरक्षा और विश्वसनीयता की प्रतिबद्धता के साथ दिए जाने वाले इंजीनियरिंग, निर्माण और धातु फैब्रिकेशन समाधान।'),

    # ---- starter services (descriptions)
    'Engineering consultancy for construction and fabrication projects.': ('निर्माण र फ्याब्रिकेसन परियोजनाका लागि इन्जिनियरिङ परामर्श।', 'निर्माण और फैब्रिकेशन परियोजनाओं के लिए इंजीनियरिंग परामर्श।'),
    'Structural design and engineering solutions in Pokhara, Nepal.': ('पोखरा, नेपालमा संरचनात्मक डिजाइन र इन्जिनियरिङ समाधान।', 'पोखरा, नेपाल में संरचनात्मक डिज़ाइन और इंजीनियरिंग समाधान।'),
    'Engineering and construction services for buildings.': ('भवनहरूका लागि इन्जिनियरिङ र निर्माण सेवाहरू।', 'इमारतों के लिए इंजीनियरिंग और निर्माण सेवाएँ।'),
    'Infrastructure engineering and construction services in Nepal.': ('नेपालमा पूर्वाधार इन्जिनियरिङ र निर्माण सेवाहरू।', 'नेपाल में बुनियादी ढाँचा इंजीनियरिंग और निर्माण सेवाएँ।'),
    'Project management and coordination for engineering and construction work.': ('इन्जिनियरिङ र निर्माण कार्यका लागि परियोजना व्यवस्थापन र समन्वय।', 'इंजीनियरिंग और निर्माण कार्य के लिए परियोजना प्रबंधन और समन्वय।'),
    'Quantity surveying and cost estimation services.': ('परिमाण सर्वेक्षण र लागत अनुमान सेवाहरू।', 'मात्रा सर्वेक्षण और लागत अनुमान सेवाएँ।'),
    'Metal fabrication company in Pokhara, Nepal — structural and custom metal fabrication.': ('पोखरा, नेपालको धातु फ्याब्रिकेसन कम्पनी — संरचनात्मक र अनुकूलित धातु फ्याब्रिकेसन।', 'पोखरा, नेपाल की धातु फैब्रिकेशन कंपनी — संरचनात्मक और कस्टम धातु फैब्रिकेशन।'),
    'Steel fabrication services for construction and industrial projects.': ('निर्माण र औद्योगिक परियोजनाका लागि स्टिल फ्याब्रिकेसन सेवाहरू।', 'निर्माण और औद्योगिक परियोजनाओं के लिए स्टील फैब्रिकेशन सेवाएँ।'),
    'Custom metal works fabricated to drawings and specifications.': ('नक्सा र विनिर्देश अनुसार बनाइएका अनुकूलित धातु कार्य।', 'ड्रॉइंग और विनिर्देशों के अनुसार बने कस्टम धातु कार्य।'),
    'Renovation and retrofitting services for existing structures.': ('विद्यमान संरचनाहरूका लागि नवीकरण र रेट्रोफिटिङ सेवाहरू।', 'मौजूदा संरचनाओं के लिए नवीनीकरण और रेट्रोफिटिंग सेवाएँ।'),
    'Maintenance services for buildings and fabricated structures.': ('भवन र फ्याब्रिकेसन गरिएका संरचनाहरूका लागि मर्मतसम्भार सेवाहरू।', 'इमारतों और फैब्रिकेटेड संरचनाओं के लिए रखरखाव सेवाएँ।'),

    # ---- starter statistics
    'Service Categories': ('सेवा वर्गहरू', 'सेवा श्रेणियाँ'),
    'Focus Area': ('मुख्य क्षेत्र', 'मुख्य क्षेत्र'),
    'Based In': ('स्थित', 'स्थित'),
    'Pokhara, Nepal': ('पोखरा, नेपाल', 'पोखरा, नेपाल'),

    # ---- starter chatbot questions and answers
    'What services do you offer?': ('तपाईंहरू कुन कुन सेवा दिनुहुन्छ?', 'आप कौन-कौन सी सेवाएँ देते हैं?'),
    'We offer engineering consultancy, structural engineering, building construction, infrastructure development, project management, quantity surveying and estimation, metal and steel fabrication, custom metal works, renovation and retrofitting, and maintenance services.': (
        'हामी इन्जिनियरिङ परामर्श, संरचनात्मक इन्जिनियरिङ, भवन निर्माण, पूर्वाधार विकास, परियोजना व्यवस्थापन, परिमाण सर्वेक्षण र लागत अनुमान, धातु तथा स्टिल फ्याब्रिकेसन, अनुकूलित धातु कार्य, नवीकरण र रेट्रोफिटिङ, तथा मर्मतसम्भार सेवा दिन्छौं।',
        'हम इंजीनियरिंग परामर्श, संरचनात्मक इंजीनियरिंग, भवन निर्माण, बुनियादी ढाँचा विकास, परियोजना प्रबंधन, मात्रा सर्वेक्षण और लागत अनुमान, धातु तथा स्टील फैब्रिकेशन, कस्टम धातु कार्य, नवीनीकरण और रेट्रोफिटिंग, तथा रखरखाव सेवाएँ देते हैं।'),
    'View our services': ('हाम्रा सेवाहरू हेर्नुहोस्', 'हमारी सेवाएँ देखें'),
    'Do you do metal fabrication?': ('के तपाईंहरू धातु फ्याब्रिकेसन गर्नुहुन्छ?', 'क्या आप धातु फैब्रिकेशन करते हैं?'),
    'Yes. Metal fabrication is a major part of our work: custom and structural steel fabrication, steel frames, gates, railings, staircases and industrial fabrication, built to drawings and specifications.': (
        'हो। धातु फ्याब्रिकेसन हाम्रो कामको ठूलो हिस्सा हो: अनुकूलित र संरचनात्मक स्टिल फ्याब्रिकेसन, स्टिल फ्रेम, गेट, रेलिङ, भ्र्याङ र औद्योगिक फ्याब्रिकेसन, नक्सा र विनिर्देश अनुसार बनाइएको।',
        'हाँ। धातु फैब्रिकेशन हमारे काम का एक बड़ा हिस्सा है: कस्टम और संरचनात्मक स्टील फैब्रिकेशन, स्टील फ्रेम, गेट, रेलिंग, सीढ़ियाँ और औद्योगिक फैब्रिकेशन, ड्रॉइंग और विनिर्देशों के अनुसार बने।'),
    'How can I get a quote?': ('म कोटेशन कसरी पाउन सक्छु?', 'मैं कोटेशन कैसे प्राप्त कर सकता हूँ?'),
    'You can send us your project details with our quote form and our team will contact you. For urgent questions, call or message us on WhatsApp.': (
        'तपाईं हाम्रो कोटेशन फारमबाट आफ्नो परियोजनाको विवरण पठाउन सक्नुहुन्छ र हाम्रो टोलीले तपाईंलाई सम्पर्क गर्नेछ। जरुरी प्रश्नका लागि फोन गर्नुहोस् वा व्हाट्सएपमा सन्देश पठाउनुहोस्।',
        'आप हमारे कोटेशन फ़ॉर्म से अपनी परियोजना का विवरण भेज सकते हैं और हमारी टीम आपसे संपर्क करेगी। जरूरी प्रश्नों के लिए कॉल करें या व्हाट्सऐप पर संदेश भेजें।'),
    'Where are you located?': ('तपाईंहरू कहाँ हुनुहुन्छ?', 'आप कहाँ स्थित हैं?'),
    'Our office is at Pokhara-14, BP Marg, Pokhara, Nepal 33700.': ('हाम्रो कार्यालय पोखरा-१४, बीपी मार्ग, पोखरा, नेपाल ३३७०० मा छ।', 'हमारा कार्यालय पोखरा-१४, बीपी मार्ग, पोखरा, नेपाल ३३७०० में है।'),
    'Contact us': ('हामीलाई सम्पर्क गर्नुहोस्', 'हमसे संपर्क करें'),
    'How can I contact you?': ('म तपाईंहरूलाई कसरी सम्पर्क गर्न सक्छु?', 'मैं आपसे कैसे संपर्क कर सकता हूँ?'),
    'You can call us on 9856082231 or email info.highnoon2019@gmail.com. You can also use the WhatsApp button or the contact form.': (
        'तपाईं हामीलाई ९८५६०८२२३१ मा फोन गर्न वा info.highnoon2019@gmail.com मा इमेल गर्न सक्नुहुन्छ। व्हाट्सएप बटन वा सम्पर्क फारम पनि प्रयोग गर्न सक्नुहुन्छ।',
        'आप हमें ९८५६०८२२३१ पर कॉल कर सकते हैं या info.highnoon2019@gmail.com पर ईमेल कर सकते हैं। आप व्हाट्सऐप बटन या संपर्क फ़ॉर्म का भी उपयोग कर सकते हैं।'),
    'Contact page': ('सम्पर्क पृष्ठ', 'संपर्क पृष्ठ'),
    'Are you hiring?': ('के तपाईंहरू भर्ना गर्दै हुनुहुन्छ?', 'क्या आप भर्ती कर रहे हैं?'),
    'Open positions are listed on our Careers page, where you can apply and upload your CV.': ('खुला पदहरू हाम्रो रोजगारी पृष्ठमा सूचीबद्ध छन्, जहाँ तपाईं आवेदन दिन र आफ्नो सीभी अपलोड गर्न सक्नुहुन्छ।', 'रिक्त पद हमारे करियर पृष्ठ पर सूचीबद्ध हैं, जहाँ आप आवेदन कर सकते हैं और अपना सीवी अपलोड कर सकते हैं।'),
    'See careers': ('रोजगारी हेर्नुहोस्', 'करियर देखें'),
    'Which projects have you done?': ('तपाईंहरूले कुन कुन परियोजना गर्नुभएको छ?', 'आपने कौन-कौन सी परियोजनाएँ की हैं?'),
    'You can see a selection of our work on the Projects page.': ('तपाईं हाम्रा कामहरूको छनोट परियोजना पृष्ठमा हेर्न सक्नुहुन्छ।', 'आप हमारे कार्यों का चयन परियोजना पृष्ठ पर देख सकते हैं।'),
    'View projects': ('परियोजनाहरू हेर्नुहोस्', 'परियोजनाएँ देखें'),

    # ---- the company's own project names
    'Multi-Storey Building with Curved Balconies': ('घुमाउरो बारेन्डा भएको बहुतले भवन', 'घुमावदार बालकनी वाली बहुमंजिला इमारत'),
    'Resort Building with Garden Courtyard': ('बगैंचासहितको चोक भएको रिसोर्ट भवन', 'बगीचे वाले आँगन के साथ रिसॉर्ट भवन'),
    'Multi-Storey Commercial Square (Night View)': ('बहुतले व्यावसायिक स्क्वायर (राति देखिने दृश्य)', 'बहुमंजिला वाणिज्यिक स्क्वायर (रात का दृश्य)'),

    # ---- project, job and news labels
    'Residential': ('आवासीय', 'आवासीय'),
    'Commercial': ('व्यावसायिक', 'वाणिज्यिक'),
    'Industrial': ('औद्योगिक', 'औद्योगिक'),
    'Institutional': ('संस्थागत', 'संस्थागत'),
    'Structural': ('संरचनात्मक', 'संरचनात्मक'),
    'Renovation': ('नवीकरण', 'नवीनीकरण'),
    'Completed': ('सम्पन्न', 'पूर्ण'),
    'Ongoing': ('जारी', 'जारी'),
    'Upcoming': ('आगामी', 'आगामी'),
    'Full-Time': ('पूर्णकालीन', 'पूर्णकालिक'),
    'Part-Time': ('अंशकालीन', 'अंशकालिक'),
    'Contract': ('करार', 'अनुबंध'),
    'Internship': ('इन्टर्नसिप', 'इंटर्नशिप'),
    'Temporary': ('अस्थायी', 'अस्थायी'),
    'Company News': ('कम्पनी समाचार', 'कंपनी समाचार'),
    'Project Update': ('परियोजना अपडेट', 'परियोजना अपडेट'),
    'Industry Insight': ('उद्योग अन्तर्दृष्टि', 'उद्योग अंतर्दृष्टि'),
    'Announcement': ('घोषणा', 'घोषणा'),
}


# The built-in director message (shown until a message is added in Admin). If you type the same
# wording in Admin -> Director messages it is translated too; for different wording add it in
# Admin -> Translations.
DATA[DEFAULT_TITLE] = ('विश्वास र गुणस्तरका साथ निर्माण', 'भरोसे और गुणवत्ता के साथ निर्माण')
DATA[DEFAULT_MESSAGE] = (
    'हाइनुन इन्जिनियरिङ सोलुसन्समा हामी विश्वास गर्छौं कि प्रत्येक संरचना विश्वासबाट सुरु हुन्छ। चाहे त्यो घर होस्, '
    'व्यावसायिक भवन होस् वा स्टिल फ्याब्रिकेसनको काम, हामी प्रत्येक परियोजनामा सावधानीपूर्वक योजना, सुरक्षित कार्यशैली '
    'र इमानदार सञ्चारलाई प्राथमिकता दिन्छौं। हाम्रो टोली बलियो, भरपर्दो र समयमै सम्पन्न कार्य उपलब्ध गराउन तथा '
    'प्रत्येक ग्राहकको परियोजनालाई आफ्नै परियोजना जस्तै ठान्न प्रतिबद्ध छ। हामीलाई रोज्नुभएकोमा धन्यवाद। '
    'हामी तपाईंसँग मिलेर दीर्घकालीन केही निर्माण गर्न उत्सुक छौं।',
    'हाईनून इंजीनियरिंग सॉल्यूशंस में हमारा मानना है कि हर संरचना की शुरुआत भरोसे से होती है। चाहे वह घर हो, '
    'व्यावसायिक इमारत हो या स्टील फैब्रिकेशन का काम, हम हर परियोजना में सावधानीपूर्वक योजना, सुरक्षित कार्यप्रणाली '
    'और ईमानदार संवाद को महत्व देते हैं। हमारी टीम मजबूत, भरोसेमंद और समय पर पूरा किया गया कार्य देने तथा '
    'हर ग्राहक की परियोजना को अपनी ही परियोजना की तरह मानने के लिए प्रतिबद्ध है। हमें चुनने के लिए धन्यवाद। '
    'हम आपके साथ मिलकर कुछ टिकाऊ बनाने के लिए उत्सुक हैं।',
)
