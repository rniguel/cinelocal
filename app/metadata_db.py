# -*- coding: utf-8 -*-
"""
Módulo de Metadados Ricos para Filmes e Séries do CineLocal.
Fornece sinopses oficiais em português do Brasil (pt-BR), elenco estelar,
diretores/criadores, gêneros, avaliações e links externos (TMDb / IMDb).
"""

import re

# =====================================================================
# SÉRIES (10 SÉRIES DO CATÁLOGO)
# =====================================================================
SERIES_METADATA = {
    'adolescence': {
        'title': 'Adolescence',
        'year': 2025,
        'overview': 'Uma crônica dramática profunda e sensível sobre os dilemas, transformações, descobertas e turbulências emocionais vividas por um grupo de jovens na transição para a vida adulta em um mundo hiperconectado.',
        'cast': ['Stephen Graham', 'Ashley Walters', 'Erin Doherty', 'Owen Cooper'],
        'creator': 'Jack Thorne & Stephen Graham',
        'genres': ['Drama', 'Crime'],
        'rating': 8.2,
        'tmdbUrl': 'https://www.themoviedb.org/tv/254885-adolescence',
        'imdbUrl': 'https://www.imdb.com/title/tt31737754/'
    },
    'arcane': {
        'title': 'Arcane',
        'year': 2021,
        'overview': 'Em meio ao conflito entre as cidades-gêmeas de Piltover e Zaun, duas irmãs lutam em lados opostos de uma guerra entre tecnologias mágicas e convicções incompatíveis.',
        'cast': ['Hailee Steinfeld', 'Ella Purnell', 'Katie Leung', 'Kevin Alejandro'],
        'creator': 'Christian Linke & Alex Yee',
        'genres': ['Animação', 'Ficção Científica', 'Ação', 'Aventura', 'Fantasia'],
        'rating': 9.0,
        'tmdbUrl': 'https://www.themoviedb.org/tv/94605-arcane',
        'imdbUrl': 'https://www.imdb.com/title/tt11126994/'
    },
    'chernobyl': {
        'title': 'Chernobyl',
        'year': 2019,
        'overview': 'Em abril de 1986, uma enorme explosão na usina nuclear de Chernobyl, na União Soviética, desencadeia um dos piores desastres causados pelo homem na história da humanidade.',
        'cast': ['Jared Harris', 'Stellan Skarsgård', 'Emily Watson', 'Paul Ritter'],
        'creator': 'Craig Mazin',
        'genres': ['Drama', 'História'],
        'rating': 9.3,
        'tmdbUrl': 'https://www.themoviedb.org/tv/87108-chernobyl',
        'imdbUrl': 'https://www.imdb.com/title/tt8462696/'
    },
    'cyberpunk': {
        'title': 'Cyberpunk: Mercenários',
        'year': 2022,
        'overview': 'Em uma distopia futurista consumida pela corrupção, violência e obsessão por implantes corporais, um jovem impulsivo e talentoso decide se tornar um edgerunner — um mercenário fora da lei em Night City.',
        'cast': ['KENN', 'Aoi Yuuki', 'Hiroki Touchi', 'Michiko Kaiden'],
        'creator': 'Rafal Jaki & Studio Trigger',
        'genres': ['Animação', 'Ação', 'Ficção Científica', 'Cyberpunk'],
        'rating': 8.3,
        'tmdbUrl': 'https://www.themoviedb.org/tv/105248-cyberpunk-edgerunners',
        'imdbUrl': 'https://www.imdb.com/title/tt12590266/'
    },
    'loki': {
        'title': 'Loki',
        'year': 2021,
        'overview': 'Após fugir com o Tesseract durante os acontecimentos de Vingadores: Ultimato, uma variante temporal do Deus da Trapaça é capturada pela misteriosa Autoridade de Variância Temporal (AVT) e forçada a consertar as linhas do tempo.',
        'cast': ['Tom Hiddleston', 'Owen Wilson', 'Sophia Di Martino', 'Gugu Mbatha-Raw'],
        'creator': 'Michael Waldron',
        'genres': ['Ficção Científica', 'Ação', 'Aventura', 'Fantasia'],
        'rating': 8.2,
        'tmdbUrl': 'https://www.themoviedb.org/tv/84958-loki',
        'imdbUrl': 'https://www.imdb.com/title/tt9140554/'
    },
    'percy jackson': {
        'title': 'Percy Jackson e os Olimpianos',
        'year': 2023,
        'overview': 'Percy Jackson é um garoto de 12 anos que descobre ser um semideus, filho de Poseidon. Quando é falsamente acusado de roubar o raio-mestre de Zeus, ele e seus amigos embarcam em uma perigosa missão pelos Estados Unidos para encontrá-lo e restaurar a paz no Olimpo.',
        'cast': ['Walker Scobell', 'Leah Sava Jeffries', 'Aryan Simhadri', 'Lin-Manuel Miranda'],
        'creator': 'Rick Riordan & Jonathan E. Steinberg',
        'genres': ['Ação', 'Aventura', 'Fantasia', 'Família'],
        'rating': 7.3,
        'tmdbUrl': 'https://www.themoviedb.org/tv/103540-percy-jackson-and-the-olympians',
        'imdbUrl': 'https://www.imdb.com/title/tt12324366/'
    },
    'pluribus': {
        'title': 'Pluribus',
        'year': 2025,
        'overview': 'Carol Sturka, a pessoa mais infeliz da Terra e uma renomada escritora, é uma das únicas sobreviventes imunes a um vírus alienígena que transformou a humanidade em uma mente coletiva eufórica. Ela agora precisa lutar para salvar o livre arbítrio do mundo contra uma felicidade forçada.',
        'cast': ['Rhea Seehorn', 'Karolina Wydra', 'Carlos Manuel Vesga'],
        'creator': 'Vince Gilligan',
        'genres': ['Ficção Científica', 'Drama', 'Suspense'],
        'rating': 8.9,
        'tmdbUrl': 'https://www.themoviedb.org/tv/225171-pluribus',
        'imdbUrl': 'https://www.imdb.com/title/tt22204992/'
    },
    'severance': {
        'title': 'Ruptura (Severance)',
        'year': 2022,
        'overview': 'Mark lidera uma equipe de funcionários na misteriosa corporação Lumon Industries, cujas memórias foram cirurgicamente separadas entre sua vida no trabalho e sua vida pessoal. Quando um colega misterioso aparece fora do escritório, uma conspiração tenebrosa começa a se desvendar.',
        'cast': ['Adam Scott', 'Patricia Arquette', 'John Turturro', 'Christopher Walken', 'Britt Lower'],
        'creator': 'Dan Erickson (Direção: Ben Stiller)',
        'genres': ['Ficção Científica', 'Suspense', 'Drama', 'Mistério'],
        'rating': 8.7,
        'tmdbUrl': 'https://www.themoviedb.org/tv/95396-severance',
        'imdbUrl': 'https://www.imdb.com/title/tt11280740/'
    },
    'the bear': {
        'title': 'O Urso (The Bear)',
        'year': 2022,
        'overview': 'Carmen Berzatto, um jovem e talentoso chef de alta gastronomia, volta a Chicago para administrar a lanchonete da sua família após a trágica morte de seu irmão mais velho, tendo que lidar com dívidas, uma cozinha caótica e uma equipe relutante.',
        'cast': ['Jeremy Allen White', 'Ebon Moss-Bachrach', 'Ayo Edebiri', 'Lionel Boyce'],
        'creator': 'Christopher Storer',
        'genres': ['Comédia', 'Drama'],
        'rating': 8.6,
        'tmdbUrl': 'https://www.themoviedb.org/tv/136283-the-bear',
        'imdbUrl': 'https://www.imdb.com/title/tt14452776/'
    },
    'wandavision': {
        'title': 'WandaVision',
        'year': 2021,
        'overview': 'Combinando o estilo clássico das sitcoms com o Universo Cinematográfico Marvel, Wanda Maximoff e Visão — dois seres superpoderosos vivendo uma vida suburbana ideal — começam a suspeitar que as coisas não são o que parecem.',
        'cast': ['Elizabeth Olsen', 'Paul Bettany', 'Kathryn Hahn', 'Teyonah Parris'],
        'creator': 'Jac Schaeffer',
        'genres': ['Ficção Científica', 'Mistério', 'Drama', 'Comédia'],
        'rating': 7.9,
        'tmdbUrl': 'https://www.themoviedb.org/tv/85271-wandavision',
        'imdbUrl': 'https://www.imdb.com/title/tt9140560/'
    }
}

# =====================================================================
# FILMES E FRANQUIAS (BASE DE DADOS COMPLETA PT-BR)
# =====================================================================
MOVIES_METADATA = {
    # Standalones clássicos
    'a origem': {
        'overview': 'Em um mundo onde é possível entrar na mente humana através dos sonhos, Dom Cobb é um ladrão experiente e o melhor na arte da extração. Ele recebe uma chance de redenção se conseguir realizar o inverso: a inserção de uma ideia.',
        'cast': ['Leonardo DiCaprio', 'Joseph Gordon-Levitt', 'Elliot Page', 'Tom Hardy'],
        'director': 'Christopher Nolan',
        'genres': ['Ação', 'Ficção Científica', 'Aventura'],
        'rating': 8.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/27205-inception',
        'imdbUrl': 'https://www.imdb.com/title/tt1375666/'
    },
    'brilho eterno de uma mente sem lembranças': {
        'overview': 'Joel se surpreende ao saber que sua namorada Clementine apagou todas as memórias do seu relacionamento tumultuado através de um procedimento experimental. Desesperado, ele decide fazer o mesmo tratamento, mas no meio do processo percebe que ainda a ama.',
        'cast': ['Jim Carrey', 'Kate Winslet', 'Kirsten Dunst', 'Mark Ruffalo'],
        'director': 'Michel Gondry',
        'genres': ['Romance', 'Drama', 'Ficção Científica'],
        'rating': 8.3,
        'tmdbUrl': 'https://www.themoviedb.org/movie/38-eternal-sunshine-of-the-spotless-mind',
        'imdbUrl': 'https://www.imdb.com/title/tt0338013/'
    },
    'clube da luta': {
        'overview': 'Um executivo deprimido que sofre de insônia conhece o carismático vendedor de sabão Tyler Durden. Juntos, eles criam um clube secreto com lutas corporais que rapidamente evolui para algo muito mais perigoso.',
        'cast': ['Brad Pitt', 'Edward Norton', 'Helena Bonham Carter', 'Meat Loaf'],
        'director': 'David Fincher',
        'genres': ['Drama', 'Suspense'],
        'rating': 8.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/550-fight-club',
        'imdbUrl': 'https://www.imdb.com/title/tt0137523/'
    },
    'como perder um homem em 10 dias': {
        'overview': 'Uma jornalista investigativa decide escrever uma matéria sobre como afastar um pretendente em 10 dias, enquanto um executivo de publicidade aposta que pode fazer qualquer mulher se apaixonar por ele no mesmo período.',
        'cast': ['Kate Hudson', 'Matthew McConaughey', 'Kathryn Hahn'],
        'director': 'Donald Petrie',
        'genres': ['Comédia', 'Romance'],
        'rating': 6.5,
        'tmdbUrl': 'https://www.themoviedb.org/movie/9919-how-to-lose-a-guy-in-10-days',
        'imdbUrl': 'https://www.imdb.com/title/tt0251127/'
    },
    'de volta para o futuro': {
        'overview': 'O jovem Marty McFly viaja acidentalmente para o ano de 1955 na máquina do tempo criada pelo excêntrico cientista Doc Brown em um DeLorean, colocando em risco sua própria existência ao alterar o passado.',
        'cast': ['Michael J. Fox', 'Christopher Lloyd', 'Lea Thompson', 'Crispin Glover'],
        'director': 'Robert Zemeckis',
        'genres': ['Aventura', 'Comédia', 'Ficção Científica'],
        'rating': 8.5,
        'tmdbUrl': 'https://www.themoviedb.org/movie/105-back-to-the-future',
        'imdbUrl': 'https://www.imdb.com/title/tt0088763/'
    },
    'garota exemplar': {
        'overview': 'No dia do seu quinto aniversário de casamento, Amy desaparece misteriosamente. Seu marido Nick se torna o principal suspeito sob a intensa pressão da mídia e de investigações policiais cheias de segredos.',
        'cast': ['Ben Affleck', 'Rosamund Pike', 'Neil Patrick Harris', 'Tyler Perry'],
        'director': 'David Fincher',
        'genres': ['Mistério', 'Suspense', 'Drama'],
        'rating': 8.1,
        'tmdbUrl': 'https://www.themoviedb.org/movie/210577-gone-girl',
        'imdbUrl': 'https://www.imdb.com/title/tt2267998/'
    },
    'gladiador': {
        'overview': 'Traído e reduzido à escravidão após o assassinato da família imperial pelo maquiavélico Cômodo, o honrado general romano Maximus busca vingança triunfando na arena do Coliseu.',
        'cast': ['Russell Crowe', 'Joaquin Phoenix', 'Connie Nielsen', 'Oliver Reed'],
        'director': 'Ridley Scott',
        'genres': ['Ação', 'Drama', 'Aventura'],
        'rating': 8.5,
        'tmdbUrl': 'https://www.themoviedb.org/movie/98-gladiator',
        'imdbUrl': 'https://www.imdb.com/title/tt0172495/'
    },
    'ilha do medo': {
        'overview': 'Em 1954, os agentes federais Teddy Daniels e Chuck Aule investigam o desaparecimento de uma assassina internada em um hospital psiquiátrico de segurança máxima em uma ilha remota.',
        'cast': ['Leonardo DiCaprio', 'Mark Ruffalo', 'Ben Kingsley', 'Michelle Williams'],
        'director': 'Martin Scorsese',
        'genres': ['Drama', 'Mistério', 'Suspense'],
        'rating': 8.2,
        'tmdbUrl': 'https://www.themoviedb.org/movie/11324-shutter-island',
        'imdbUrl': 'https://www.imdb.com/title/tt1130884/'
    },
    'la la land': {
        'overview': 'Em Los Angeles, um pianista de jazz dedicado e uma atriz iniciante se apaixonam enquanto tentam equilibrar seus sonhos profissionais e ambições artísticas na cidade das estrelas.',
        'cast': ['Ryan Gosling', 'Emma Stone', 'John Legend', 'J.K. Simmons'],
        'director': 'Damien Chazelle',
        'genres': ['Comédia', 'Drama', 'Romance', 'Música'],
        'rating': 8.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/313369-la-la-land',
        'imdbUrl': 'https://www.imdb.com/title/tt3783958/'
    },
    'matrix': {
        'overview': 'Um jovem programador descobre que o mundo em que vive é uma simulação virtual criada por máquinas inteligentes para escravizar a raça humana e se une a um grupo de rebeldes.',
        'cast': ['Keanu Reeves', 'Laurence Fishburne', 'Carrie-Anne Moss', 'Hugo Weaving'],
        'director': 'Lana & Lilly Wachowski',
        'genres': ['Ação', 'Ficção Científica'],
        'rating': 8.7,
        'tmdbUrl': 'https://www.themoviedb.org/movie/603-the-matrix',
        'imdbUrl': 'https://www.imdb.com/title/tt0133093/'
    },
    'o diabo veste prada': {
        'overview': 'Uma jovem recém-formada e ingênua consegue um disputado emprego como assistente de Miranda Priestly, a implacável e temida editora de uma das maiores revistas de moda de Nova York.',
        'cast': ['Meryl Streep', 'Anne Hathaway', 'Emily Blunt', 'Stanley Tucci'],
        'director': 'David Frankel',
        'genres': ['Comédia', 'Drama'],
        'rating': 6.9,
        'tmdbUrl': 'https://www.themoviedb.org/movie/350-the-devil-wears-prada',
        'imdbUrl': 'https://www.imdb.com/title/tt0458352/'
    },
    'o drama': {
        'overview': 'Às vésperas do casamento de um casal aparentemente perfeito, revelações inesperadas e segredos do passado vêm à tona, transformando o que deveria ser um dia de celebração em um turbilhão de incertezas.',
        'cast': ['Zendaya', 'Robert Pattinson', 'Mamoudou Athie', 'Alana Haim'],
        'director': 'Kristoffer Borgli',
        'genres': ['Comédia', 'Romance', 'Drama'],
        'rating': 7.6,
        'tmdbUrl': 'https://www.themoviedb.org/movie/1329249-the-drama',
        'imdbUrl': 'https://www.imdb.com/title/tt32925232/'
    },
    'o show de truman': {
        'overview': 'Um pacato vendedor de seguros descobre aos poucos que toda a sua vida, desde o nascimento, é o reality show mais assistido do planeta e que todas as pessoas ao seu redor são atores contratados.',
        'cast': ['Jim Carrey', 'Laura Linney', 'Ed Harris', 'Noah Emmerich'],
        'director': 'Peter Weir',
        'genres': ['Comédia', 'Drama', 'Ficção Científica'],
        'rating': 8.2,
        'tmdbUrl': 'https://www.themoviedb.org/movie/37165-the-truman-show',
        'imdbUrl': 'https://www.imdb.com/title/tt0120382/'
    },
    'obsessão': {
        'overview': 'Um suspense psicológico intenso onde relações conturbadas e segredos perigosos culminam em uma espiral de desconfiança e obsessão quando limites éticos são ultrapassados.',
        'cast': ['Zendaya', 'Josh O\'Connor', 'Mike Faist'],
        'director': 'Luca Guadagnino',
        'genres': ['Romance', 'Drama', 'Suspense'],
        'rating': 7.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/937287-challengers',
        'imdbUrl': 'https://www.imdb.com/title/tt16426418/'
    },
    'parasita': {
        'overview': 'Toda a família de Ki-taek está desempregada, vivendo em um porão sujo. Uma oportunidade surge para o filho começar a dar aulas para a herdeira de uma família rica, dando início a um plano engenhoso de infiltração.',
        'cast': ['Song Kang-ho', 'Lee Sun-kyun', 'Cho Yeo-jeong', 'Choi Woo-shik'],
        'director': 'Bong Joon-ho',
        'genres': ['Comédia', 'Suspense', 'Drama'],
        'rating': 8.5,
        'tmdbUrl': 'https://www.themoviedb.org/movie/496243-parasite',
        'imdbUrl': 'https://www.imdb.com/title/tt6751668/'
    },
    'pulp fiction': {
        'overview': 'As vidas de dois assassinos da máfia, um boxeador trapaceiro, a esposa de um gângster poderoso e um casal de assaltantes de lanchonete se entrelaçam em quatro contos de violência e redenção.',
        'cast': ['John Travolta', 'Samuel L. Jackson', 'Uma Thurman', 'Bruce Willis'],
        'director': 'Quentin Tarantino',
        'genres': ['Suspense', 'Crime'],
        'rating': 8.9,
        'tmdbUrl': 'https://www.themoviedb.org/movie/680-pulp-fiction',
        'imdbUrl': 'https://www.imdb.com/title/tt0110912/'
    },
    'simplesmente acontece': {
        'overview': 'Os jovens britânicos Rosie e Alex são amigos inseparáveis desde a infância. Apesar de sentirem uma atração mútua indiscutível, o destino insiste em colocá-los em caminhos e relacionamentos separados.',
        'cast': ['Lily Collins', 'Sam Claflin', 'Christian Cooke', 'Jaime Winstone'],
        'director': 'Christian Ditter',
        'genres': ['Comédia', 'Romance'],
        'rating': 7.1,
        'tmdbUrl': 'https://www.themoviedb.org/movie/253412-love-rosie',
        'imdbUrl': 'https://www.imdb.com/title/tt1638360/'
    },
    'um sonho de liberdade': {
        'overview': 'Condenado à prisão perpétua pelo assassinato da esposa e do amante que alega não ter cometido, o banqueiro Andy Dufresne desenvolve uma amizade profunda com o prisioneiro veterano Red.',
        'cast': ['Tim Robbins', 'Morgan Freeman', 'Bob Gunton', 'William Sadler'],
        'director': 'Frank Darabont',
        'genres': ['Drama', 'Crime'],
        'rating': 9.3,
        'tmdbUrl': 'https://www.themoviedb.org/movie/278-the-shawshank-redemption',
        'imdbUrl': 'https://www.imdb.com/title/tt0111161/'
    },

    # --- NOVOS FILMES AVULSOS ADICIONADOS ---
    'a fantástica fábrica de chocolate': {
        'overview': 'Willy Wonka é o excêntrico dono da maior fábrica de doces do mundo. Ele decide realizar um concurso mundial escondendo cinco convites dourados em suas barras de chocolate para escolher seu sucessor.',
        'cast': ['Johnny Depp', 'Freddie Highmore', 'David Kelly', 'Helena Bonham Carter'],
        'director': 'Tim Burton',
        'genres': ['Aventura', 'Comédia', 'Família', 'Fantasia'],
        'rating': 6.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/118-charlie-and-the-chocolate-factory',
        'imdbUrl': 'https://www.imdb.com/title/tt0367594/'
    },
    'a grande aposta': {
        'overview': 'Em 2008, o excêntrico investidor Michael Burry percebe que o mercado imobiliário dos EUA está prestes a colapsar devido a empréstimos podres. Ele aposta contra os bancos e cria um mercado financeiro bilionário.',
        'cast': ['Christian Bale', 'Steve Carell', 'Ryan Gosling', 'Brad Pitt'],
        'director': 'Adam McKay',
        'genres': ['Comédia', 'Drama', 'História'],
        'rating': 7.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/318846-the-big-short',
        'imdbUrl': 'https://www.imdb.com/title/tt1596363/'
    },
    'backrooms': {
        'overview': 'Um misterioso fenômeno dimensional faz com que pessoas caiam em um labirinto infinito de salas vazias de paredes amarelas e lâmpadas fluorescentes, perseguidos por entidades sobrenaturais nos limites da realidade.',
        'cast': ['Chiwetel Ejiofor', 'Renate Reinsve', 'Mark Duplass', 'Finn Bennett'],
        'director': 'Kane Parsons',
        'genres': ['Terror', 'Ficção Científica', 'Mistério'],
        'rating': 7.5,
        'tmdbUrl': 'https://www.themoviedb.org/movie/1083381-the-backrooms',
        'imdbUrl': 'https://www.imdb.com/title/tt26685816/'
    },
    'blade runner 2049': {
        'overview': 'Trinta anos após os acontecimentos do primeiro filme, o policial K desenterra um segredo enterrado há muito tempo que tem o potencial de mergulhar o que resta da sociedade no caos e parte em busca do lendário Rick Deckard.',
        'cast': ['Ryan Gosling', 'Harrison Ford', 'Ana de Armas', 'Sylvia Hoeks'],
        'director': 'Denis Villeneuve',
        'genres': ['Ficção Científica', 'Mistério', 'Drama'],
        'rating': 8.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/335984-blade-runner-2049',
        'imdbUrl': 'https://www.imdb.com/title/tt1856101/'
    },
    'diário de uma paixão': {
        'overview': 'Na década de 1940, o humilde operário Noah Calhoun e a rica herdeira Allie se apaixonam perdidamente durante um verão na Carolina do Sul. Separados pela família e pela Segunda Guerra Mundial, o amor sobrevive ao longo das décadas.',
        'cast': ['Ryan Gosling', 'Rachel McAdams', 'James Garner', 'Gena Rowlands'],
        'director': 'Nick Cassavetes',
        'genres': ['Drama', 'Romance'],
        'rating': 7.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/11036-the-notebook',
        'imdbUrl': 'https://www.imdb.com/title/tt0332280/'
    },
    'dois caras legais': {
        'overview': 'Na Los Angeles dos anos 1970, o detetive particular atrapalhado Holland March e o brutamontes de aluguel Jackson Healy são forçados a trabalhar juntos para desvendar o desaparecimento de uma jovem e a morte de uma estrela pornô.',
        'cast': ['Ryan Gosling', 'Russell Crowe', 'Angourie Rice', 'Matt Bomer'],
        'director': 'Shane Black',
        'genres': ['Comédia', 'Crime', 'Ação'],
        'rating': 7.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/290250-the-nice-guys',
        'imdbUrl': 'https://www.imdb.com/title/tt3799694/'
    },
    'drive': {
        'overview': 'Um piloto habilidoso trabalha como dublê de cinema durante o dia e motorista de fuga para criminosos durante a noite. Sua vida solitária muda ao se aproximar de sua vizinha Irene e de seu filho, mas um assalto fracassado o coloca na mira da máfia.',
        'cast': ['Ryan Gosling', 'Carey Mulligan', 'Bryan Cranston', 'Albert Brooks'],
        'director': 'Nicolas Winding Refn',
        'genres': ['Drama', 'Ação', 'Suspense', 'Crime'],
        'rating': 7.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/64690-drive',
        'imdbUrl': 'https://www.imdb.com/title/tt0780504/'
    },
    'esposa de mentirinha': {
        'overview': 'Danny Maccabee é um cirurgião plástico bem-sucedido que mente usando uma aliança falsa para evitar compromissos sérios. Quando se apaixona por Palmer, ele precisa convencer sua leal assistente Katherine a fingir ser sua ex-esposa em um fim de semana no Havaí.',
        'cast': ['Adam Sandler', 'Jennifer Aniston', 'Nicole Kidman', 'Nick Swardson'],
        'director': 'Dennis Dugan',
        'genres': ['Comédia', 'Romance'],
        'rating': 6.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/50546-just-go-with-it',
        'imdbUrl': 'https://www.imdb.com/title/tt1564364/'
    },
    'golpe baixo': {
        'overview': 'Paul Crewe, um ex-astro do futebol americano preso por dirigir embriagado, é coagido pelo diretor de uma penitenciária federal a formar um time de detentos para enfrentar a sádica equipe de guardas da prisão.',
        'cast': ['Adam Sandler', 'Chris Rock', 'Burt Reynolds', 'Nelly'],
        'director': 'Peter Segal',
        'genres': ['Comédia', 'Crime'],
        'rating': 6.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/9291-the-longest-yard',
        'imdbUrl': 'https://www.imdb.com/title/tt0398165/'
    },
    'juntos e misturados': {
        'overview': 'Após um primeiro encontro desastroso às cegas, os pais solteiros Lauren e Jim viajam separadamente com seus filhos para um resort de luxo na África do Sul e acabam presos na mesma suíte durante uma semana inteira.',
        'cast': ['Adam Sandler', 'Drew Barrymore', 'Kevin Nealon', 'Terry Crews'],
        'director': 'Frank Coraci',
        'genres': ['Comédia', 'Romance'],
        'rating': 6.5,
        'tmdbUrl': 'https://www.themoviedb.org/movie/232672-blended',
        'imdbUrl': 'https://www.imdb.com/title/tt1086772/'
    },
    'o lobo de wall street': {
        'overview': 'Durante os anos 1990, o corretor da bolsa de valores Jordan Belfort constrói um império financeiro fraudulento na corretora Stratton Oakmont, mergulhando em um estilo de vida de ostentação desenfreada, festas, drogas e perseguição pelo FBI.',
        'cast': ['Leonardo DiCaprio', 'Jonah Hill', 'Margot Robbie', 'Matthew McConaughey'],
        'director': 'Martin Scorsese',
        'genres': ['Crime', 'Drama', 'Comédia'],
        'rating': 8.2,
        'tmdbUrl': 'https://www.themoviedb.org/movie/106646-the-wolf-of-wall-street',
        'imdbUrl': 'https://www.imdb.com/title/tt0993846/'
    },
    'supergirl': {
        'overview': 'Diferente de seu primo Kal-El criado por pais amorosos na Terra, Kara Zor-El cresceu vendo Krypton se despedaçar ao seu redor. Em sua jornada pelo cosmos com seu fiel cão Krypto, ela busca sua própria identidade e justiça.',
        'cast': ['Milly Alcock', 'Eve Ridley', 'Matthias Schoenaerts'],
        'director': 'Craig Gillespie',
        'genres': ['Ação', 'Aventura', 'Ficção Científica'],
        'rating': 7.6,
        'tmdbUrl': 'https://www.themoviedb.org/movie/1081003-supergirl-woman-of-tomorrow',
        'imdbUrl': 'https://www.imdb.com/title/tt26443588/'
    },
    'superman': {
        'overview': 'Superman tenta conciliar sua herança extraterrestre kryptoniana com sua criação humana como Clark Kent em Smallville. Sendo a personificação da verdade e da justiça, ele é guiado pela bondade humana em um mundo que vê a compaixão como antiquada.',
        'cast': ['David Corenswet', 'Rachel Brosnahan', 'Nicholas Hoult', 'Edi Gathegi'],
        'director': 'James Gunn',
        'genres': ['Ação', 'Aventura', 'Ficção Científica'],
        'rating': 8.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/1061474-superman',
        'imdbUrl': 'https://www.imdb.com/title/tt5950044/'
    },
    'the odyssey': {
        'overview': 'Após a brutal queda de Tróia, o rei Odisseu e seus guerreiros enfrentam a fúria dos deuses, monstros mitológicos, sereias sedutoras e os perigos do mar aberto em uma jornada de dez anos para retornar a Ítaca e salvar sua rainha Penélope.',
        'cast': ['Dominic Keating', 'Myrom Kingery', 'Morgan Flanagan', 'Patrick M. Byrnes'],
        'director': 'Marcel Walz',
        'genres': ['Aventura', 'Ação', 'Fantasia'],
        'rating': 6.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/1329249-the-odyssey',
        'imdbUrl': 'https://www.imdb.com/title/tt32925230/'
    },
    # Universo Cinematográfico Marvel (MCU & Deadpool)
    'capitão américa - o primeiro vingador': {
        'overview': 'Durante a Segunda Guerra Mundial, o jovem e franzino Steve Rogers se voluntaria para o projeto militar ultra-secreto Renascimento. Transformado no supersoldado Capitão América, ele lidera a luta contra as forças nazistas e a terrível organização Hidra comandada pelo Caveira Vermelha.',
        'cast': ['Chris Evans', 'Hayley Atwell', 'Sebastian Stan', 'Hugo Weaving', 'Tommy Lee Jones'],
        'director': 'Joe Johnston',
        'genres': ['Ação', 'Aventura', 'Ficção Científica'],
        'rating': 7.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/1771-captain-america-the-first-avenger',
        'imdbUrl': 'https://www.imdb.com/title/tt0458339/'
    },
    'os vingadores': {
        'overview': 'Quando Loki obtém acesso ao Tesseract e ameaça escravizar a Terra, Nick Fury, diretor da S.H.I.E.L.D., reúne os heróis mais poderosos do planeta na lendária iniciativa Vingadores para deter a invasão alienígena Chitauri.',
        'cast': ['Robert Downey Jr.', 'Chris Evans', 'Mark Ruffalo', 'Chris Hemsworth', 'Scarlett Johansson', 'Tom Hiddleston'],
        'director': 'Joss Whedon',
        'genres': ['Ação', 'Ficção Científica', 'Aventura'],
        'rating': 8.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/24428-the-avengers',
        'imdbUrl': 'https://www.imdb.com/title/tt0848228/'
    },
    'vingadores - era de ultron': {
        'overview': 'Ao tentar criar um programa pacifista de inteligência artificial chamado Ultron para proteger a Terra, Tony Stark acidentalmente dá origem a uma força maligna e autoconsciente que decide aniquilar a humanidade.',
        'cast': ['Robert Downey Jr.', 'Chris Hemsworth', 'Mark Ruffalo', 'Chris Evans', 'James Spader', 'Elizabeth Olsen'],
        'director': 'Joss Whedon',
        'genres': ['Ação', 'Ficção Científica', 'Aventura'],
        'rating': 7.3,
        'tmdbUrl': 'https://www.themoviedb.org/movie/99861-avengers-age-of-ultron',
        'imdbUrl': 'https://www.imdb.com/title/tt2395427/'
    },
    'capitão américa - guerra civil': {
        'overview': 'O governo decide impor uma lei para regulamentar e monitorar as atividades dos Vingadores. O debate ético cria uma fratura violenta entre Steve Rogers, que defende a liberdade sem amarras, e Tony Stark, que apoia o controle estatal.',
        'cast': ['Chris Evans', 'Robert Downey Jr.', 'Scarlett Johansson', 'Sebastian Stan', 'Anthony Mackie', 'Chadwick Boseman'],
        'director': 'Anthony & Joe Russo',
        'genres': ['Ação', 'Ficção Científica', 'Aventura'],
        'rating': 7.8,
        'tmdbUrl': 'https://www.themoviedb.org/movie/271110-captain-america-civil-war',
        'imdbUrl': 'https://www.imdb.com/title/tt3498820/'
    },
    'deadpool 2': {
        'overview': 'Quando o soldado cibernético Cable viaja no tempo com a missão letal de eliminar um jovem mutante angustiado, o irreverente mercenário Deadpool recruta um esquadrão excêntrico de heróis improváveis, batizado de X-Force.',
        'cast': ['Ryan Reynolds', 'Josh Brolin', 'Morena Baccarin', 'Julian Dennison', 'Zazie Beetz'],
        'director': 'David Leitch',
        'genres': ['Ação', 'Comédia', 'Ficção Científica'],
        'rating': 7.7,
        'tmdbUrl': 'https://www.themoviedb.org/movie/383498-deadpool-2',
        'imdbUrl': 'https://www.imdb.com/title/tt5463162/'
    },
    'deadpool': {
        'overview': 'O ex-militar das Forças Especiais Wade Wilson descobre que está com câncer terminal e aceita participar de uma experiência clandestina. Sobrevivendo com fator de cura acelerado e senso de humor sombrio, ele adota o alter-ego de Deadpool para caçar seus algozes.',
        'cast': ['Ryan Reynolds', 'Morena Baccarin', 'Ed Skrein', 'T.J. Miller'],
        'director': 'Tim Miller',
        'genres': ['Ação', 'Comédia', 'Ficção Científica'],
        'rating': 8.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/293660-deadpool',
        'imdbUrl': 'https://www.imdb.com/title/tt1431045/'
    },
    'vingadores - guerra infinita': {
        'overview': 'O déspota cósmico Thanos inicia uma caçada implacável pelas seis Joias do Infinito, pretendendo utilizá-las para erradicar metade de todas as vidas do universo. Os Vingadores e os Guardiões da Galáxia enfrentam seu maior desafio até então.',
        'cast': ['Robert Downey Jr.', 'Chris Hemsworth', 'Mark Ruffalo', 'Chris Evans', 'Josh Brolin', 'Benedict Cumberbatch'],
        'director': 'Anthony & Joe Russo',
        'genres': ['Ação', 'Ficção Científica', 'Aventura'],
        'rating': 8.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/299536-avengers-infinity-war',
        'imdbUrl': 'https://www.imdb.com/title/tt4154756/'
    },
    'vingadores - ultimato': {
        'overview': 'Cinco anos após Thanos dizimar metade do universo com um estalar de dedos, os Vingadores remanescentes se unem em um ousado plano de assalto temporal através do Reino Quântico para recuperar as Joias e restaurar todos os perdidos.',
        'cast': ['Robert Downey Jr.', 'Chris Evans', 'Mark Ruffalo', 'Chris Hemsworth', 'Scarlett Johansson', 'Paul Rudd'],
        'director': 'Anthony & Joe Russo',
        'genres': ['Ação', 'Ficção Científica', 'Aventura'],
        'rating': 8.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/299534-avengers-endgame',
        'imdbUrl': 'https://www.imdb.com/title/tt4154796/'
    },
    'homem-aranha - sem volta para casa': {
        'overview': 'Com sua identidade secreta revelada ao mundo pelo Mysterio, Peter Parker pede a ajuda do Doutor Estranho para conjurar um feitiço de esquecimento. O feitiço é corrompido, rasgando o tecido do multiverso e trazendo icônicos vilões de outras realidades.',
        'cast': ['Tom Holland', 'Zendaya', 'Benedict Cumberbatch', 'Jacob Batalon', 'Willem Dafoe', 'Alfred Molina'],
        'director': 'Jon Watts',
        'genres': ['Ação', 'Aventura', 'Ficção Científica'],
        'rating': 8.2,
        'tmdbUrl': 'https://www.themoviedb.org/movie/634649-spider-man-no-way-home',
        'imdbUrl': 'https://www.imdb.com/title/tt10872600/'
    },
    'doutor estranho no multiverso da loucura': {
        'overview': 'Doutor Estranho precisa atravessar realidades alternativas assustadoras e desconcertantes para proteger a jovem America Chavez da corrupção sombria e implacável da Feiticeira Escarlate possuída pelo Darkhold.',
        'cast': ['Benedict Cumberbatch', 'Elizabeth Olsen', 'Chiwetel Ejiofor', 'Benedict Wong', 'Xochitl Gomez'],
        'director': 'Sam Raimi',
        'genres': ['Fantasia', 'Ação', 'Aventura', 'Terror'],
        'rating': 7.0,
        'tmdbUrl': 'https://www.themoviedb.org/movie/453395-doctor-strange-in-the-multiverse-of-madness',
        'imdbUrl': 'https://www.imdb.com/title/tt9419884/'
    },
    'deadpool & wolverine': {
        'overview': 'Vivendo tranquilamente como vendedor e afastado dos combates, Wade Wilson é convocado pela Autoridade de Variância Temporal (AVT) em uma crise que ameaça sua linha do tempo. Desesperado, ele recruta uma variante alternativa e amargurada de Wolverine.',
        'cast': ['Ryan Reynolds', 'Hugh Jackman', 'Emma Corrin', 'Matthew Macfadyen', 'Morena Baccarin'],
        'director': 'Shawn Levy',
        'genres': ['Ação', 'Comédia', 'Ficção Científica'],
        'rating': 7.9,
        'tmdbUrl': 'https://www.themoviedb.org/movie/533535-deadpool-wolverine',
        'imdbUrl': 'https://www.imdb.com/title/tt6263850/'
    },
    'capitão américa - admirável mundo novo': {
        'overview': 'Sam Wilson assume plenamente as responsabilidades do escudo do Capitão América. Após um encontro com o recém-eleito presidente dos EUA Thaddeus Ross, ele se vê imerso em uma conspiração internacional de proporções mundiais.',
        'cast': ['Anthony Mackie', 'Harrison Ford', 'Giancarlo Esposito', 'Liv Tyler', 'Shira Haas'],
        'director': 'Julius Onah',
        'genres': ['Ação', 'Ficção Científica', 'Suspense'],
        'rating': 7.2,
        'tmdbUrl': 'https://www.themoviedb.org/movie/823464-captain-america-brave-new-world',
        'imdbUrl': 'https://www.imdb.com/title/tt14513804/'
    },
    'thunderbolts': {
        'overview': 'Uma equipe de operações secretas formada por anti-heróis, mercenários e ex-assassinos do MCU — incluindo Yelena Belova, Bucky Barnes e o Guardião Vermelho — é mobilizada pelo governo americano para missões de alto risco das quais ninguém mais pode escapar.',
        'cast': ['Florence Pugh', 'Sebastian Stan', 'David Harbour', 'Wyatt Russell', 'Julia Louis-Dreyfus', 'Hannah John-Kamen'],
        'director': 'Jake Schreier',
        'genres': ['Ação', 'Aventura', 'Crime'],
        'rating': 7.4,
        'tmdbUrl': 'https://www.themoviedb.org/movie/986056-thunderbolts',
        'imdbUrl': 'https://www.imdb.com/title/tt20969586/'
    },
    'quarteto fantástico - primeiros passos': {
        'overview': 'Em uma deslumbrante Nova York retrofuturista dos anos 1960 em uma realidade alternativa, Reed Richards, Sue Storm, Johnny Storm e Ben Grimm formam a Primeira Família da Marvel e são forçados a defender seu mundo contra o devorador de planetas Galactus e seu misterioso arauto, o Surfista Prateado.',
        'cast': ['Pedro Pascal', 'Vanessa Kirby', 'Joseph Quinn', 'Ebon Moss-Bachrach', 'Ralph Ineson', 'Julia Garner'],
        'director': 'Matt Shakman',
        'genres': ['Ficção Científica', 'Ação', 'Aventura'],
        'rating': 7.6,
        'tmdbUrl': 'https://www.themoviedb.org/movie/617126-the-fantastic-four-first-steps',
        'imdbUrl': 'https://www.imdb.com/title/tt10676052/'
    }
}

def get_series_info(series_folder_name):
    key = series_folder_name.lower().strip()
    for k, v in SERIES_METADATA.items():
        if k in key or key in k:
            return v
    return {
        'title': series_folder_name,
        'year': 2024,
        'overview': f'Série completa com todas as temporadas disponíveis em alta definição no CineLocal.',
        'cast': ['Elenco Principal'],
        'creator': 'Produção Original',
        'genres': ['Série', 'Drama'],
        'rating': 8.0,
        'tmdbUrl': f'https://www.themoviedb.org/search?query={series_folder_name}',
        'imdbUrl': f'https://www.imdb.com/find/?q={series_folder_name}'
    }

def get_movie_info(title, year=0, franchise=None):
    clean = title.lower()
    clean = re.sub(r'^\d{2}\s*-\s*', '', clean)
    clean = re.sub(r'\s*\(\d{4}\)', '', clean)
    clean = clean.strip()
    
    # 1. Match exato ou parcial na base de filmes
    for k, v in MOVIES_METADATA.items():
        if k in clean or clean in k:
            info = dict(v)
            if not info.get('year'):
                info['year'] = year
            return info
            
    # 2. Informações de franquias
    if franchise:
        f_low = franchise.lower()
        if 'shrek' in f_low:
            return {
                'overview': f'A hilária e inesquecível aventura no Reino de Tão Tão Distante com Shrek, Burro e a Princesa Fiona.',
                'cast': ['Mike Myers', 'Eddie Murphy', 'Cameron Diaz', 'Antonio Banderas'],
                'director': 'Andrew Adamson & Vicky Jenson',
                'genres': ['Animação', 'Comédia', 'Família', 'Fantasia'],
                'rating': 7.9,
                'tmdbUrl': 'https://www.themoviedb.org/search?query=Shrek',
                'imdbUrl': 'https://www.imdb.com/find/?q=Shrek'
            }
        elif 'homem-aranha' in f_low:
            return {
                'overview': f'Peter Parker ganha habilidades extraordinárias após ser picado por uma aranha geneticamente modificada e aprende que com grandes poderes vêm grandes responsabilidades.',
                'cast': ['Tobey Maguire', 'Kirsten Dunst', 'Willem Dafoe', 'James Franco'],
                'director': 'Sam Raimi',
                'genres': ['Ação', 'Aventura', 'Ficção Científica'],
                'rating': 7.4,
                'tmdbUrl': 'https://www.themoviedb.org/collection/556-spider-man-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Spider-Man'
            }
        elif 'beetlejuice' in f_low:
            return {
                'overview': f'O fantasma bioexorcista Beetlejuice espalha caos, comédia e sustos extravagantes entre os vivos e os mortos.',
                'cast': ['Michael Keaton', 'Winona Ryder', 'Catherine O\'Hara', 'Jenna Ortega'],
                'director': 'Tim Burton',
                'genres': ['Comédia', 'Fantasia', 'Terror'],
                'rating': 7.3,
                'tmdbUrl': 'https://www.themoviedb.org/search?query=Beetlejuice',
                'imdbUrl': 'https://www.imdb.com/find/?q=Beetlejuice'
            }
        elif 'piratas do caribe' in f_low:
            return {
                'overview': f'As lendárias aventuras e desventuras em alto-mar do excêntrico e imprevisível Capitão Jack Sparrow.',
                'cast': ['Johnny Depp', 'Geoffrey Rush', 'Orlando Bloom', 'Keira Knightley'],
                'director': 'Gore Verbinski',
                'genres': ['Aventura', 'Ação', 'Fantasia'],
                'rating': 8.0,
                'tmdbUrl': 'https://www.themoviedb.org/collection/295-pirates-of-the-caribbean-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Pirates+of+the+Caribbean'
            }
        elif 'velozes e furiosos' in f_low:
            return {
                'overview': f'Corridas clandestinas em alta velocidade, missões de espionagem internacional e a inquebrável lealdade à família de Dominic Toretto.',
                'cast': ['Vin Diesel', 'Paul Walker', 'Michelle Rodriguez', 'Dwayne Johnson'],
                'director': 'Justin Lin & James Wan',
                'genres': ['Ação', 'Crime', 'Suspense'],
                'rating': 7.2,
                'tmdbUrl': 'https://www.themoviedb.org/collection/9485-the-fast-and-the-furious-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Fast+and+Furious'
            }
        elif 'harry potter' in f_low:
            return {
                'overview': f'A jornada mágica do jovem bruxo Harry Potter na Escola de Magia e Bruxaria de Hogwarts contra as forças das trevas.',
                'cast': ['Daniel Radcliffe', 'Emma Watson', 'Rupert Grint'],
                'director': 'Chris Columbus / David Yates',
                'genres': ['Aventura', 'Fantasia', 'Família'],
                'rating': 7.8,
                'tmdbUrl': 'https://www.themoviedb.org/collection/1241-harry-potter-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Harry+Potter'
            }
        elif 'marvel' in f_low:
            return {
                'overview': f'Os maiores heróis da Terra e do universo se unem para proteger a humanidade contra ameaças intergalácticas no Universo Cinematográfico Marvel.',
                'cast': ['Robert Downey Jr.', 'Chris Evans', 'Chris Hemsworth', 'Scarlett Johansson'],
                'director': 'Anthony & Joe Russo',
                'genres': ['Ação', 'Aventura', 'Ficção Científica'],
                'rating': 8.0,
                'tmdbUrl': 'https://www.themoviedb.org/collection/86311-the-avengers-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Marvel'
            }
        elif 'star wars' in f_low:
            return {
                'overview': f'Há muito tempo, em uma galáxia muito, muito distante... A épica batalha entre a Ordem Jedi e os Sith pelo destino da galáxia.',
                'cast': ['Mark Hamill', 'Harrison Ford', 'Carrie Fisher'],
                'director': 'George Lucas',
                'genres': ['Ficção Científica', 'Ação', 'Aventura'],
                'rating': 8.6,
                'tmdbUrl': 'https://www.themoviedb.org/collection/10-star-wars-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Star+Wars'
            }
        elif 'senhor dos anéis' in f_low:
            return {
                'overview': f'A jornada da Sociedade do Anel para destruir o Um Anel na Montanha da Perdição e salvar a Terra-média do Lorde das Trevas Sauron.',
                'cast': ['Elijah Wood', 'Ian McKellen', 'Viggo Mortensen', 'Orlando Bloom'],
                'director': 'Peter Jackson',
                'genres': ['Aventura', 'Fantasia', 'Ação'],
                'rating': 8.9,
                'tmdbUrl': 'https://www.themoviedb.org/collection/119-the-lord-of-the-rings-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Lord+of+the+Rings'
            }
        elif 'batman' in f_low:
            return {
                'overview': f'O Cavaleiro das Trevas patrulha as ruas sombrias de Gotham City, combatendo a corrupção e os vilões mais perigosos do crime organizado.',
                'cast': ['Christian Bale', 'Heath Ledger', 'Michael Caine', 'Gary Oldman'],
                'director': 'Christopher Nolan',
                'genres': ['Ação', 'Crime', 'Drama'],
                'rating': 8.5,
                'tmdbUrl': 'https://www.themoviedb.org/collection/263-the-dark-knight-collection',
                'imdbUrl': 'https://www.imdb.com/find/?q=Batman'
            }

    # 3. Fallback inteligente
    return {
        'overview': f'Filme completo em alta resolução disponível no CineLocal.',
        'cast': ['Elenco Principal'],
        'director': 'Direção Especial',
        'genres': ['Filme', 'Cinema'],
        'rating': 7.5,
        'tmdbUrl': f'https://www.themoviedb.org/search?query={title}',
        'imdbUrl': f'https://www.imdb.com/find/?q={title}'
    }
