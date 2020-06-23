from ilabs.aclient.ilabs_predictor import ILabsPredictor
import trio

async def demo():
    predictor = ILabsPredictor.init(domain='ilabs.bib')

    out = await predictor.api.ping()
    print('ping:', out)

    bibliography_brs = '''<brs:b xmlns:brs="http://innodatalabs.com/brs">

    <brs:r>Lucas Theis, Aäron van den Oord, and Matthias Bethge. A note on the \
    evaluation of generative models. ICLR, 2016.</brs:r>

    <brs:r>Luc Devroye. Sample-based non-uniform random variate generation. \
    Springer-Verlag, New York, 1986.</brs:r>

    </brs:b>
    '''.encode('utf-8')

    out = await predictor(bibliography_brs, progress=print)
    print('predictor:', out)


if __name__ == '__main__':
    trio.run(demo)