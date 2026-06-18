from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" ADD "indicator_card_id" VARCHAR(60);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "metric" DROP COLUMN "indicator_card_id";"""


MODELS_STATE = (
    "eJztXW1v2joU/iuIT6vEndqu7ab7DSjVuGuhaum906oqMomBqMbJErMOTf3v184LsfMCCQ"
    "olKefT6Mk5if3Ex+c5x3b2pzlmmouRo8+08fPHtoPRaGnj5t+NP02K5uJHhkar0US2Hb8u"
    "xAyNiWeIuK7GQuWxyxykM35hgoiLucjAru6YNjMtyqV0QYgQWjpXNOk0Ei2o+XOBNWZNMZ"
    "thh194fOJikxr4N3bDP+1nbWJiYihtNw3xbE/ut4TLujPkXHma4nFjTbfIYk4jbXvJZhZd"
    "qfPWCOkUU+wghg2pA6J9QWdDkd9WLmDOAq8aaUQCA0/QgjCpwzlR0C0qEDQpc70uztFvjW"
    "A6ZTP+5/nxq9+ZqKu+lujBv+277tf23Yfz46Pmq6eHGPI1PfQiuHhvMCmC2MqgjqCdnp/n"
    "QI1r+bBFMC1sQ3RKQyyJ1SW/wsw5TsdLtYyBZgSmH8Mf20AYCiIMI3crCUTu1saQkmXwft"
    "ZgOOrf9O5H7Ztb0ZO56/4kHkTtUU9cOfWky5j0w8WRkFt8svCnkdVNGv/1R18b4s/Gj+Gg"
    "5yFouWzqeE+M9EY/mqJNaMEsjVovGjKkoRRKw8aLqWPyLHmDEIyR/vyCHENTrkQDwLbIcs"
    "pRSb7+TmB59e0OE+RBm3zRyox669+rmu/6NRzAoVSGzTq1snBLXpqfzuMSRNHUa7V4tniS"
    "gkvXIgTrQYMzopGkkyMe6ap2ZQJSn7IC8Ui8hNhYCYb2XmfWqXjKX6cnZ5/Pvny6OPvCVb"
    "yWrCSf18wT/cFoQ2Ty/i0QmEL9Osalk+M80ZxrQVyCuKR4yRxziPRSwtKNdyt1gq3eO99j"
    "fLq87WYHJnExR0QybB1CUd1CUfDSVOCuiIUyoAv0Y9hNhEGlnSoNncvhQ+e617i963X79/"
    "3hQJ0pvYtCxAUm87p512tfx6KUjbRCQ2+lv3n0VQO/cgagAlhR+iOZlMOA3gA1lQPlqmic"
    "nAMHesccSHECP00uOHUoRoc0fyToYwLJlBhmOdic0m946aHZ541CVE+bROpfwOBiB72sWF"
    "FspPAfBibYD2Hd9n23fdlrvmYz8N2zTZ+ONzMJZ3A9B+ecR5pAOyvmtetoJ1RAclRALFv0"
    "ygz7WwCupGVNiRMUj4A4ye+VY2bqiFmOpotYVHBFNM14K8cIWro3v7jI4xYXnldsVXqLFh"
    "eg/JYxAMvDpS/fsqawhIyzxJptwMQjLlhTaHxINJPhefm4XKMlrtu4eav8Is+aa9rMlC/n"
    "0GABtr7ph+lqtmPOkbNM8UjLIhjRDAwVw7ibcstK+2IaWJ3h8Frhfp3+SGV3g4ebTo+z7C"
    "O1GJ4s7QLpfp+kO5rpihUsE3aHVLNMowBFwFNsDgm4NcXeqNpXSq23jtSyFSv1KsMkvdKb"
    "7sqloVjXtC6OZGK2qmrdPMoXN9BaJbHMyWqV/BZIbdUmx7WkNrs0kaMmdnDVdWCr75OtAt"
    "kCsrU/srVPehDuXcikBdLmhk10QNpXsVMW8NicIXfWfAI2UDIb8GAtQARC/VLWw2py9G2K"
    "LeHSKUXAf+6Hg3ScZJsYVg+Ud+OR8ynWahDTZU+Vnu3SsBLdVqL8IETvpv09FtEH3ethJx"
    "6+xQ06MZTfdK/Hvldmtx6L4nxxSrDN3okdGsBW7HC7zGRi6iYiHCOj2G6ZuGEN50BIgyAN"
    "SswnXg8KbpKJ29Vz41iBTwisSYGUbz6UkgXJX5yoHoZ586D4GCmaCm04flR8T0RwQq0+iK"
    "ZULGDTDGyaybnZyrGYUElZw9kCGX6zbnCvGuHxZtWUTWcVEh6Xs7Ki7erowqNcuwke8gRr"
    "L7uttvxCZIFTZqrsOkJkAVWEPFUEyFPeZ54CyzXbHqSGM6RwhnS/Z0iTfgzLhbVbLpRzon"
    "wsd5U/FaO6Xja3C74bDT3Jk8XDAuh1glxX/AYavGMavEI6gV52wVG2qWexcevauzRGc+/X"
    "ikwODCwiZh1t4RT8pKtkVE/A4MOukDFBxgQZU5UyJiD725D9lLEIOWedvlu0WivJzpOk1Z"
    "SN2ZG8jANHLao2/bXW5Dni1aW4bvZmrdAANmuF5JQWxjAyARQ3rwRvGIwrK8BSxnJBt0Mz"
    "sgM8If181+knZFGw7nTAOUAb8zRv1szMAILrrRz/o1ikCeS/Yl7bWrfXBztu6gcUssvQks"
    "mBFaGFExQAKlCvJ0hbL23wuzJMU3hS9vYxyQT2j8VJTrh/LBF73zJwvP4P5ZkzAw=="
)
