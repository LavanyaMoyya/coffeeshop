from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Coffeeshop, Base, MenuItem, User

engine = create_engine('sqlite:///coffeeshopmenuwithusers.db')
"""Bind the engine to the metadata of the Base class so that the
declaratives can be accessed through a DBSession instance"""
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
"""A DBSession() instance establishes all conversations with the database
 and represents a "staging zone" for all the objects loaded into the
 database session object. Any change made against the objects in the
 session won't be persisted into the database until you call
 session.commit(). If you're not happy about the changes, you can
 revert all of them back to the last commit by calling
 session.rollback()"""
session = DBSession()


"""Create user"""
User1 = User(name="Lavanya", email="lavanyamoyya3@gmail.com",
             picture='https://lh6.googleusercontent.com'
             '/-ODf1V0QoS2Q/AAAAAAAAAAI/AAAAAAAAAAA/'
             'saglyR2exWU/W96-H96/photo.jpg')
session.add(User1)
session.commit()

"""Menu for Baristas"""
coffeeshop1 = Coffeeshop(user_id=1, name="Baristas")
session.add(coffeeshop1)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Espresso",
                     description='''The espresso (aka short black)
                     is the foundation and the most important part
                     to every espresso based drink mayo and lettuce''',
                     price="$7.50",
                     picture="https://tinyurl.com/y4yktkov",
                     variety="Coffee", coffeeshop=coffeeshop1)
session.add(menuItem1)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Short Macchiato",
                     description='''A short macchiato is similar to
                     an espresso but with a dollop of steamed milk
                     and foam to mellow the harsh taste of an espresso.''',
                     price="$2.99",
                     picture="https://tinyurl.com/y5f85bnu",
                     variety="Coffee", coffeeshop=coffeeshop1)
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Vanilla Ice Cream",
                     description='''Vanilla ice cream, like other flavors
                     of ice cream, was originally created by cooling a
                     mixture made of cream, sugar, and vanilla
                     above a container of ice and salt.''',
                     price="$5.50",
                     picture="https://tinyurl.com/y5486njw",
                     variety="Icecream", coffeeshop=coffeeshop1)
session.add(menuItem2)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Rocky road",
                     description='''Rocky road ice cream is a chocolate
                     flavored ice cream. Though there are variations
                     on the flavor, it is traditionally composed of
                     chocolate ice cream, nuts, and marshmallows.''',
                     price="$3.99",
                     picture="https://tinyurl.com/y4zw66la",
                     variety="Icecream", coffeeshop=coffeeshop1)
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Basil Lemonade",
                     description='''This tangy basil-infused
                     drink is made for summer.''',
                     price="$7.99",
                     picture="https://tinyurl.com/yxzs8kqt",
                     variety="Cooldrink", coffeeshop=coffeeshop1)
session.add(menuItem3)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Hibiscus Mocktini",
                     description='''In a pitcher, mix together the hibiscus
                     tea and ginger ale. Serve over ice in a tall
                     glass with a fresh pineapple spear.''',
                     price="$1.99",
                     picture="https://tinyurl.com/y6rcof49",
                     variety="Cooldrink", coffeeshop=coffeeshop1)
session.add(menuItem3)
session.commit()

"""Menu for Tatiana's Cafe"""
coffeeshop2 = Coffeeshop(user_id=1, name="Tatiana's Cafe")
session.add(coffeeshop2)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Ristretto",
                     description='''A ristretto is an espresso shot that is
                     extracted with the same amount of coffee
                     but half the amount of water.''',
                     price="$7.50",
                     picture="https://tinyurl.com/y3d5vyxc",
                     variety="Coffee", coffeeshop=coffeeshop2)
session.add(menuItem1)
session.commit()


menuItem1 = MenuItem(user_id=1, name="Long Black (Americano)",
                     description='''A long black (aka americano)
                     is hot water with an espresso shot
                     extracted on top of the hot water.''',
                     price="$2.99",
                     picture="https://tinyurl.com/y4nvqqqp",
                     variety="Coffee", coffeeshop=coffeeshop2)
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name=" Peanut butter cup",
                     description='''A peanut butter cup is a
                     molded chocolate candy with a
                     peanut butter filling inside.''',
                     price="$5.50",
                     picture="https://tinyurl.com/y258xe5v",
                     variety="Icecream", coffeeshop=coffeeshop2)
session.add(menuItem2)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Neapolitan ice cream",
                     description='''Neapolitan ice cream, sometimes known
                     as harlequin ice cream, is made up of blocks of
                     vanilla,chocolate, and strawberry ice cream
                     side by side in the same container.''',
                     price="$3.99",
                     picture="https://tinyurl.com/yxjaxhsn",
                     variety="Icecream", coffeeshop=coffeeshop2)
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Ginger Beer",
                     description='''strain the ginger-beer base
                     into a pitcher.Thinly slice the remaining
                     lemon and orange to form circles.''',
                     price="$7.99",
                     picture="https://tinyurl.com/y2k39nw8",
                     variety="Cooldrink", coffeeshop=coffeeshop2)
session.add(menuItem3)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Iced Tea Four Ways",
                     description='''Remove and discard the bags
                     and allow the tea to cool to room temperature.
                     Stir in the honey and ginger and refrigerate
                     until ready to use. Serve over ice.''',
                     price="$1.99",
                     picture="https://tinyurl.com/yymwff66",
                     variety="Cooldrink", coffeeshop=coffeeshop2)
session.add(menuItem3)
session.commit()

"""Menu for Dream Bean Coffee Shop"""
coffeeshop3 = Coffeeshop(user_id=1, name="Dream Bean Coffee Shop")
session.add(coffeeshop3)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Cafe Latte",
                     description='''A cafe latte, or latte for short,
                     is an espresso based drink with steamed milk and
                     micro-foam added to the coffee.''',
                     price="$7.50",
                     picture="https://tinyurl.com/y2lbkqju",
                     variety="Coffee", coffeeshop=coffeeshop3)
session.add(menuItem1)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Cappuccino",
                     description='''A cappuccino is similar to a latte.
                     However the key difference between a latte and
                     cappuccino is that a cappuccino has more foam and
                     chocolate placed on top of the drink.''',
                     price="$2.99",
                     picture="https://tinyurl.com/y4dncsju",
                     variety="Coffee", coffeeshop=coffeeshop3)
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Chocolate brownie",
                     description='''A variation made with brown sugar
                     and chocolate bits but without melted chocolate
                     in the batter is called a blonde brownie.''',
                     price="$5.50",
                     picture="https://tinyurl.com/yyjehlbe",
                     variety="Icecream", coffeeshop=coffeeshop3)
session.add(menuItem2)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Dulce de leche",
                     description='''Dulce de leche is a confection prepared
                     by slowly heating sweetened milk to create a substance
                     that derives its taste from the Maillard reaction,
                     changing flavour and colour.''',
                     price="$3.99",
                     picture="https://tinyurl.com/y5l66m8t",
                     variety="Icecream", coffeeshop=coffeeshop3)
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Espresso Slushy",
                     description=''''a fork, crush the mixture every 30 minutes
                     until it is firm but not frozen hard
                     (should be slightly slushy), about 2 hours.''',
                     price="$7.99",
                     picture="https://tinyurl.com/y34uv34m",
                     variety="Cooldrink", coffeeshop=coffeeshop3)
session.add(menuItem3)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Raspberry Fizz",
                     description='''In a large pitcher, combine 1/2 cup of lime
                     syrup with the cranberry juice,
                     seltzer, and ginger ale.''',
                     price="$1.99",
                     picture="https://tinyurl.com/y5jy78xp",
                     variety="Cooldrink", coffeeshop=coffeeshop3)
session.add(menuItem3)
session.commit()

"""Menu for The Coffee Club"""
coffeeshop4 = Coffeeshop(user_id=1, name="The Coffee Club")
session.add(coffeeshop4)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Flat White",
                     description='''It is made the same as a cappuccino expect
                     it does not have any foam or chocolate on top.''',
                     price="$7.50",
                     picture="https://tinyurl.com/y39s69zo",
                     variety="Coffee", coffeeshop=coffeeshop4)
session.add(menuItem1)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Piccolo Latte",
                     description='''A piccolo latte is a cafe latte made
                     in an espresso cup. This means it has a very strong
                     but mellowed down espresso taste thanks to
                     the steamed milk and micro foam within it.''',
                     price="$2.99",
                     picture="https://tinyurl.com/y3bp5alm",
                     variety="Coffee", coffeeshop=coffeeshop4)
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Butter Pecan",
                     description='''Butter pecan is a flavor, prominent
                     especially in the United States, in
                     cakes, cookies, and ice cream.
                     Roasted pecans, butter, and vanilla flavor
                     are used in butter pecan baked goods.''',
                     price="$5.50",
                     picture="https://tinyurl.com/y62prjrn",
                     variety="Icecream", coffeeshop=coffeeshop4)
session.add(menuItem2)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Rainbow sherbet",
                     description='''Rainbow sherbet is a frozen dessert
                     made with the foundations in ice cream,
                     milk and sugar; however,sherbet also contains
                     a frozen mixture of sweetened fruit juice,
                     water, which may contain milk,egg whites
                     and/or gelatin, orange, raspberry,
                     lime, lemon, or pineapple flavors.''',
                     price="$3.99",
                     picture="https://tinyurl.com/yym9n4y5",
                     variety="Icecream", coffeeshop=coffeeshop4)
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Iced Green Tea With Ginger and Mint",
                     description='''In a large saucepan over high heat, combine
                     the ginger and 6 cups of water and bring to a boil.''',
                     price="$7.99",
                     picture="https://tinyurl.com/yyd62hus",
                     variety="Cooldrink", coffeeshop=coffeeshop4)
session.add(menuItem3)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Watermelon-Mint Cooler",
                     description='''In a blender, puree the watermelon
                     and lemonade; strain if desired.''',
                     price="$1.99",
                     picture="https://tinyurl.com/y2bhtv8v",
                     variety="Cooldrink", coffeeshop=coffeeshop4)
session.add(menuItem3)
session.commit()

""" Menu for Wake Up Cafe"""
coffeeshop5 = Coffeeshop(user_id=1, name="Wake Up Cafe")
session.add(coffeeshop5)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Mocha",
                     description='''A mocha is a mix between a cappuccino
                     and a hot chocolate. It is made by putting mixing
                     chocolate powder with an espresso shot and then
                     adding steamed milk and micro-foam into the beverage.''',
                     price="$7.50",
                     picture="https://tinyurl.com/y32q36dc",
                     variety="Coffee", coffeeshop=coffeeshop5)
session.add(menuItem1)
session.commit()

menuItem1 = MenuItem(user_id=1, name="Affogato",
                     description='''An affogato is a simple dessert coffee
                     that is treat during summer and after dinner.
                     It is made by placing one big scoope of vanilla ice cream
                     within a single or double shot of espresso.''',
                     price="$2.99",
                     picture="https://tinyurl.com/y5homyee",
                     variety="Coffee", coffeeshop=coffeeshop5)
session.add(menuItem1)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Banana split",
                     description='''A banana split is an ice cream-based
                     dessert.In its classic form it is served in a
                     long dish called a boat.A banana is cut in half
                     lengthwise and laid in the dish.''',
                     price="$5.50",
                     picture="https://tinyurl.com/y2nzfbry",
                     variety="Icecream", coffeeshop=coffeeshop5)
session.add(menuItem2)
session.commit()

menuItem2 = MenuItem(user_id=1, name="Butterscotch",
                     description='''Butterscotch is a type of confectionery
                     whose primary ingredients are brown sugar and butter,
                     although other ingredients such as corn syrup, cream,
                     vanilla,and salt are part of some recipes.''',
                     price="$3.99",
                     picture="https://tinyurl.com/yxslnc85",
                     variety="Icecream", coffeeshop=coffeeshop5)
session.add(menuItem2)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Cucumber and Lime Spritzer",
                     description='''In a pitcher, combine the club soda, lime
                     juice,and cucumber. Serve over ice.''',
                     price="$7.99",
                     picture="https://tinyurl.com/y4ened7m",
                     variety="Cooldrink", coffeeshop=coffeeshop5)
session.add(menuItem3)
session.commit()

menuItem3 = MenuItem(user_id=1, name="Frozen Blueberry Lemonade",
                     description='''In a blender, puree the blueberries,
                     lemonade,mint, confectioners' sugar, and
                     3 cups ice until smooth.''',
                     price="$1.99",
                     picture="https://tinyurl.com/yysc2kld",
                     variety="Cooldrink", coffeeshop=coffeeshop5)
session.add(menuItem3)
session.commit()
print("added menu items!")
