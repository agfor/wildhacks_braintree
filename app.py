from flask import Flask, redirect, url_for, render_template, request, flash

import braintree

app = Flask(__name__)

gateway = braintree.Configuration.configure(
    braintree.Environment.Sandbox,
    'pgd875t7kmgp5q6x',
    'hyzkhx8dmp7xfg5h',
    '1efb7f31c4f358206b1298923ae48a6a'
)

def attribute_list(object):
    return sorted((key, getattr(object, key)) for key in object._setattrs)

@app.route('/')
def new_checkout():
    client_token = braintree.ClientToken.generate()
    return render_template('new.html', client_token=client_token)

@app.route('/checkout', methods=['POST'])
def create_checkout():
    result = braintree.Transaction.sale({
        'amount': request.form['amount'],
        'payment_method_nonce': request.form['payment_method_nonce'],
    })
    if result.is_success:
        return render_template('show.html',
                transaction = attribute_list(result.transaction))
    elif result.transaction:
        flash('Transaction status - %s' % result.transaction.status)
        return render_template('show.html',
                transaction = attribute_list(result.transaction))
    else:
        for error in result.errors.deep_errors:
            flash(error.message)
        return redirect(url_for('new_checkout'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
