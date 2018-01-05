from category import Category
from item import Item

from index import Session, engine, Base

Base.metadata.create_all(engine)
session = Session()

# Categories

characters_category = Category('Characters')
planets_category = Category('Planets')
ships_category = Category('Space Ships')
factions_category = Category('Factions')
technologies_category = Category('Technologies')
episodes_category = Category('Episodes')


# Characters

ed_mercer = Item(
    'Captain Ed Mercer',
    'Ed Mercer is the Human captain of the USS Orville. He is portrayed by Seth MacFarlane.'
)

kelly_grayson = Item(
    'Commander Kelly Grayson',
    'Kelly Grayson is a Commander and First Officer of the USS Orville.'
)

bortus = Item(
    'Lt. Commander Bortus',
    'Bortus is a Moclan crew member of the The Orville. He comes from a single gender species with cultural and behavioral attitudes that are quite different from other species that are members of the Planetary Union. For this reason, Captain Mercer and the rest of The Orville\'s crew aren\'t quite sure how to communicate with him. He has a mate named Klyden who lives onboard the ship alongside him, with their son Topa.'
)


# Planets

earth = Item(
    'Earth',
    'Earth is a planet in, and capital of the Planetary Union. It is home to the space-capable species, Humans.'
)

xelaya = Item(
    'Xelaya',
    'Xelaya is a member world of the Planetary Union, home to the Xelayan species.'
)

moclus = Item(
    'Moclus',
    'Moclus is a planet and member of the Planetary Union. It is the home of the all-male Moclan species. Moclus is notable as its surface is entirely industrialized.'
)


# Space Ships

orville = Item(
    'USS Orville',
    'The USS Orville, or ECV-197, is a mid-level exploratory vessel in Planetary Union service in the early 25th century.'
)

olympia = Item(
    'USS Olympia',
    'The USS Olympia or LCV-529 is a Leviathan-class heavy cruiser for the Planetary Union commanded by Admiral Ozawa.'
)

yakar = Item(
    'Yakar',
    'The Yakar is a Krill destroyer formerly led by Captain Haros. Sometime in late 2419 or early 2420, the Yakar was captured by the Planetary Union. It is currently under Union possession.'
)


# Factions

union = Item(
    'Planetary Union',
    'The Planetary Union is a federation of space flight-capable species, based at Planetary Union Central on Earth. The Union consists of science and exploratory vessels, a unified military, and a quasi-government overseeing affairs among colonies. According to Admiral Tucker and Captain Ed Mercer, the combined Union fleet of the year 2419 is roughly 3,000 vessels.[1] The Union\'s history is almost completely obscure, including details of its foundation and development.'
)

krill = Item(
    'Krill',
    'The Krill are an aggressive reptilian species whom antagonize the Planetary Union in 2419, particularly despising humans. As such, they have been engaged by the USS Orville on multiple occasions. The species itself originates on a planet covered in a shroud of darkness. Because of this, sunlight is lethal, and causes them to burn up.'
)

sargus = Item(
    'Sargus 4',
    'Sargus 4 is a planet resembling Earth in the 21st century. It was encountered by the USS Orville in the episode Majority Rule. Similar to Earth, Sargas 4 appears to have large bodies of water around it\'s surface as well as land with diverse vegetation.'
)


# Technologies

quantum_drive = Item(
    'Quantum drive',
    'The Quantum Drive is the main propulsion system of The Orville as well as most Planetary Union starships. Its power source is dysonium.'
)

dermoscanner = Item(
    'Dermoscanner',
    'A dermoscanner is a medical instrument capable of healing cuts and abrasions used by medical officers within the Planetary Union.'
)

holographic_generator = Item(
    'Holographic generator',
    'The holographic generator is a device that uses holograms to create fake images to fool the perception of lifeforms as well as bioscanners.'
)


# Episodes

episode_majority_rule = Item(
    'Majority Rule',
    'Majority Rule is the seventh episode of season one of The Orville. Lieutenant John LaMarr is arrested by the police of a developing planet, and it is up to the crew of the USS Orville to rescue him. The title refers to the planet\'s government by pure democracy.'
)

episode_krill = Item(
    'Krill',
    'Krill is the sixth episode of the first season of The Orville. Captain Ed Mercer and Lieutenant Gordon Malloy of the USS Orville go undercover aboard a Krill ship.'
)

episode_if_the_stars_should_appera = Item(
    'If the Stars Should Appear',
    'If the Stars Should Appear is the fourth episode of the first season of The Orville. The USS Orville finds an alien ship adrift in space and on course to collide with a nearby star, only to discover inside a species that is completely unaware of their plight.'
)


# Items into categories

characters_category.items = [ed_mercer, kelly_grayson, bortus]
planets_category.items = [earth, xelaya, moclus]
ships_category.items = [orville, olympia, yakar]
factions_category.items = [union, krill, sargus]
technologies_category.items = [quantum_drive, dermoscanner, holographic_generator]
episodes_category.items = [episode_majority_rule, episode_krill, episode_if_the_stars_should_appera]


# Adding to session

session.add(characters_category)
session.add(planets_category)
session.add(ships_category)
session.add(factions_category)
session.add(technologies_category)
session.add(episodes_category)


# Commit and close

session.commit()
session.close()