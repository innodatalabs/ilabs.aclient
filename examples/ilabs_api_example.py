# coding: utf-8
from ilabs.aclient.ilabs_api import ILabsApi
import trio

async def demo():
    api = ILabsApi()  # uses indirect authentication
    out = await api.ping()
    print('ping:', out)

    bibliography_brs = '''<brs:b xmlns:brs="http://innodatalabs.com/brs">

    <brs:r>Lucas Theis, Aäron van den Oord, and Matthias Bethge. A note on the \
    evaluation of generative models. ICLR, 2016.</brs:r>

    <brs:r>Luc Devroye. Sample-based non-uniform random variate generation. \
    Springer-Verlag, New York, 1986.</brs:r>

    </brs:b>
    '''.encode('utf-8')

    out = await api.upload_input(bibliography_brs)
    print('upload_input:', out)

    input_filename = out['input_filename']

    out = await api.download_input(input_filename)
    print('download_input:', out)
    assert out == bibliography_brs

    out = await api.predict('ilabs.bib', input_filename)
    print('predict:', out)
    task_id = out['task_id']
    output_filename = out['output_filename']

    for _ in range(10):
        print('Waiting for asynchronous job to complete...')
        await trio.sleep(1)

        out = await api.status('ilabs.bib', task_id)
        print('status:', out)
        if out['completed']:
            break
    else:
        assert False, 'Timeout'

    assert out.get('error') is None, out

    out = await api.download_output(output_filename)
    print('get:', out)

    bibliography_expected_output = b'<?xml version=\'1.0\' encoding=\'utf-8\'?>\n<brs:b xmlns:brs="http://innodatalabs.com/brs">\n<brs:r c="6.04'
    assert out.startswith(bibliography_expected_output), out[:len(bibliography_expected_output)]

    out = await api.upload_feedback('ilabs.bib', '000000-000000-0000-00000000.html', bibliography_expected_output)
    print('upload_feedback', out)


if __name__ == '__main__':
    trio.run(demo)