![Fast Data Science logo](https://raw.githubusercontent.com/fastdatascience/brand/main/primary_logo.svg)

<a href="https://fastdatascience.com"><span align="left">🌐 fastdatascience.com</span></a>
<a href="https://www.linkedin.com/company/fastdatascience/"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/linkedin.svg" alt="Fast Data Science | LinkedIn" width="21px"/></a>
<a href="https://twitter.com/fastdatascienc1"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/x.svg" alt="Fast Data Science | X" width="21px"/></a>
<a href="https://www.instagram.com/fastdatascience/"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/instagram.svg" alt="Fast Data Science | Instagram" width="21px"/></a>
<a href="https://www.facebook.com/fastdatascienceltd"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/fb.svg" alt="Fast Data Science | Facebook" width="21px"/></a>
<a href="https://www.youtube.com/channel/UCLPrDH7SoRT55F6i50xMg5g"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/yt.svg" alt="Fast Data Science | YouTube" width="21px"/></a>
<a href="https://g.page/fast-data-science"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/google.svg" alt="Fast Data Science | Google" width="21px"/></a>
<a href="https://medium.com/fast-data-science"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/medium.svg" alt="Fast Data Science | Medium" width="21px"/></a>
<a href="https://mastodon.social/@fastdatascience"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/mastodon.svg" alt="Fast Data Science | Mastodon" width="21px"/></a>

# Drug named entity recognition Python library by Fast Data Science

<!-- badges: start -->
![my badge](https://badgen.net/badge/Status/In%20Development/orange)

[![PyPI package](https://img.shields.io/badge/pip%20install-drug_named_entity_recognition-brightgreen)](https://pypi.org/project/drug-named-entity-recognition/) [![version number](https://img.shields.io/pypi/v/drug-named-entity-recognition?color=green&label=version)](https://github.com/fastdatascience/drug_named_entity_recognition/releases) [![License](https://img.shields.io/github/license/fastdatascience/drug_named_entity_recognition)](https://github.com/fastdatascience/drug_named_entity_recognition/blob/main/LICENSE)

<!-- badges: end -->

# 💊 Drug named entity recognition

Developed by Fast Data Science, https://fastdatascience.com

Source code at https://github.com/fastdatascience/drug_named_entity_recognition

Tutorial at https://fastdatascience.com/drug-named-entity-recognition-python-library/

This is a lightweight Python library for finding drug names in a string, otherwise known as [named entity recognition (NER)](https://fastdatascience.com/named-entity-recognition/) and named entity linking.

Please note this library finds only high confidence drugs and doesn't support misspellings at present.

It also only finds the English names of these drugs. Names in other languages are not supported.

It also doesn't find short code names of drugs, such as abbreviations commonly used in medicine, such as "Ceph" for "Cephradin" - as these are highly ambiguous.


# Interested in other kinds of named entity recognition (NER)? 💸Finances, 🎩company names, 🌎countries, 🗺️locations, proteins, 🧬genes, 🧪molecules?

If your NER problem is common across industries and likely to have been seen before, there may be an off-the-shelf NER tool for your purposes, such as our [Country Named Entity Recognition](http://fastdatascience.com//country-named-entity-recognition/) Python library. Dictionary-based named entity recognition is not always the solution, as sometimes the total set of entities is an open set and can't be listed (e.g. personal names), so sometimes a bespoke trained NER model is the answer. For tasks like finding email addresses or phone numbers, regular expressions (simple rules) are sufficient for the job.

If your named entity recognition or named entity linking problem is very niche and unusual, and a product exists for that problem, that product is likely to only solve your problem 80% of the way, and you will have more work trying to fix the final mile than if you had done the whole thing manually. Please [contact Fast Data Science](http://fastdatascience.com//contact) and we'll be glad to discuss. For example, we've worked on [a consultancy engagement to find molecule names in papers, and match author names to customers](http://fastdatascience.com//boehringer-ingelheim-finding-molecules-and-proteins-in-scientific-literature/) where the goal was to trace molecule samples ordered from a pharma company and identify when the samples resulted in a publication. For this case, there was no off-the-shelf library that we could use.

For a problem like identifying country names in English, which is a closed set with well-known variants and aliases, and an off-the-shelf library is usually available.

For identifying a set of molecules manufactured by a particular company, this is the kind of task more suited to a [consulting engagement](https://fastdatascience.com/portfolio/nlp-consultant/).


<img align="left" alt="Google Sheets logo" title="Google Sheets logo" width=150 height=105  src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAJYAAABpCAIAAABXp015AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAAB3RJTUUH5wsQFSwhj+n9fwAAGHNJREFUeNrtXVlwVFd6/v9ze1d3S40QatCOhBY2sQ5msQUYjMf2eBbDjJ24ah7iykylUvOQ92TynqqkKpXKjCuplBk7k3hmzMSObTBgxmIRSIBAgLW1kEAb2qVWt9Tq7nvPn4e79L29CDACbjt8COi+99xF57v/Of96LnLi8AzZDPa0b+AZHhXPKMx6PKMw6/GMwqzHMwqzHs8ozHo8ozDrYXnaN/DQoIdsj0/7hh83TEohAQEAput/BB2ND8APqa1IOQy/ZaSakUICQkAgICB8qA5PJ6Eqf4DqI0HfLtE0HYUaf6D7sEjrBwAqfzXZBvo2iaLpKAQAIECAOOc3JvoujwemY3OgdLw2GCY1lyWWMhCKnPjm/NUvl2yxCgIBfLuE0IQUEgBQTJL+s/ur/+g6PRoJSsAJCEBhSGZK/ayQyokoIbCkPxkRSFw6VLzZZ8/ZsaLGKlgAaBExzLph1nwUAiDgV0M3//nWpyExIgATAAlQppCACBEASGZSnd9QIZiSJJWICAEY40BXJ3sl4jsLa22CVX4QFp9os4VI01GIgHEuHR+4Ohuft6CgbU8eJBGBCO83G6IyAAMHkoiuTvYSwG5/nVWwyEMvLiaN2QFTUUgEiIhxLo0uzCS2KsKnaTeg3/WAYIAMUeS8dbJXAPacv8YqWJBQmUAx1YBB/cnNLJGmojABDiT/gG5glAdP7UvaA9PKpUwPEQEiJ7o80QMAO/21FsGiEEWqJqw8JmamLBmmo1CzAEBPHhICUkap05v6lNiGingRcQJSmDGyaBUsCU0Wk86IkA1kms5Hqlcp9d2XZDKQbnsagdSrp0RJgyQiSsBbJgIXRzrjkihPh6iMnIlLm588GaajUFM2QbMcVGlURlGVNEp7rPoJ9adIAQJygCuTt5tHuuJiXFFqskaDMcBEA6miWOhGUZ0sJRqR8RuqNoa2DUB1xqhMJ54J9QMiApFIUvNEgAM956+1MgEVezHLmDSVFKLuX0XmyPjZSFSyyzrRnvRtdX4BbYtqVUrAmycCTSMdIpcS5mVWwUQUojr/YAoxGQ+RGyjSRkZ9B5NPngES55cnemQWETDrSDTPQEpJcSQiyuQR1RpoZFPC1waAgIip82VaEuWhU9ZRBcAd/lqLIKj+N9KOM7ONaCIpBF3vUOYfPUgGJOgiSO/uXhBjyiUwWToREAEkUkbUuCRiYqTNgonRXBQmmYSpc2ESMsYuNE4VerEvOBqORTTpTHNhRJGoeTxwfqQ9zkVE1GQw09VNArNRSPfdRCq0nXSf0xEijC4Em4bbY/G4hQmMMYbIEBGRIWOMMYayB46Ark7cbhrtFCUJtcOBcLFx4Snza5650AA5/pc07ZBhvNT9Z4xA6c8CiSAvXJ/sC4bDdblFTqsdGVOOQ0xSV5lEg6MjMzPB12p3Csxsj3gamIdC1IfqKN2spoWTEt90n7TtaSxEAADiDHuiY713hoU5iZHqJUhRVpFQ4tLg5OjBqm0um8P8DlPzUAipfZUyPCnhQExqkHaSTHt2xshtlSyMIpLsciWeprBL5EBWli25Gaai0IBUadPvwjSNSPc3/ewkp82QXZAAICoBADCGpBNXAkAgzjTZND+PpqIwyTRMaxcq/FDypqT9ie8J55p+j40BAMQkACCWIv2IwMzPnQJTUaiCAIg4qQOmPvi6aMjXyJKqEyX26IAANiZnWVHCglfBDUFgk0+HpqIw0VHpA0vGtkm6TjJ/OrWG0h6LgDYBECHODcoRIqn0oen5AzNRmOgrzECl9l31nmjTV3ovtob0oXzZh2ZFAgRRu7YSFjY9cQmYh8JkZDCYdRmIOmUm3eQHGWZTAI0/uakVAQEk+SlSHGuEepUJ05/FHDAXhapkJcTLuDNla4ryqU8yzXiV1MQ1CxISSEoKjZE/s8NcFCpYzI4wqDYp5KXd82CXEpAQQDT4A9Ll5JgOJnIgGQZDkENNpP6khgOT+1QvV/edypKj/PJRDEGQrRoCTN1vUphICg1avT4FPwUExIlzIqMSq1dBSZFb0h+iYwvRAkxJTtRrnQICAnGk7MheAzAPhWQMFnLOKcXNDercJyBuza/yCE4OXL9jEXAgUhdJIoA5KXp96o5u2SS9UQHIFgvzZ/L7PC2YhUKtC9CooSTmwERaG3ksjr/b9JM6b5H04EtXJexGtKBwI3j37cZ/mhUjqv2esAAR9V7Y5NswIcxCoYykbkoXQiICYsgEOeAHyHR1F/IZOBDnHBAYMpZsD5BEXEAUMHm79q/O7WoMdejaLX7bTxjmolAPSmPVyU7ohIHfFx4/1t8scgkRZRVEIr5l+eoX/RuA4NPBKzem7wqJ/BqwMuFI+a7ynALdIE2GSTONC9aAVLaeurpjVgplPTSNSa2EcAFAQDa8MP2rzhNRLmo9G+fi25UNB1fWc6KTw9c+7GuyMkE+TCLustj2+NeudhfKjbUk/2Rhf+q0PAzMSuFiMCiWiMgMZUlIxBGQKYm9yJCBHGVEQUCmukeVxCeDMyAZpp3+DMhGCmUgAORYHGvzimNc1LaKXFrpXEZARFSUk7/OV6IvUrQLFpfFLn8mzZzQe+QyR5FNC7NSuFjIXEkqE7lU61l19PlfoNE6tKJFnkf/uu6Vn9cewsRRAABOZuPEZenjSslw4ljDRbIEZqUQUjsxSecAAIhzcSIya5zFKNfqcgpWAAjHIrNiROcOJQRc6fQ5wKqeJo39kHUwLYWUYovpAxBERAxZ++zgLy7+e1Q/kJJ0pHzn3278MSD8S+fn/9PfYmECACAiATkE678+97Pt+VXpr6hDFhFrVgppEc2eNHsjzqWJWCgqxbWRN05iWIzKKb+heGQyFrIyC6hxQLtgiZNkKFvU/km+ftbArBQCQIbUeq1uQkCmNiLVvEMiIs61XGEkRKVClLiumlQ55lswjJqZQjIa3ZiyVyJe7Vn1D9t+qnOzISe+2lMIAIj456tf2LOiTjYqZN8ZA6x0+7NIwh4E5qUQAEDJ6NYst4RmgoAcqMDuPVy+W6kHVXdxIok4EOwoqNm5olYNIit1vHEuJimixgtq588amJTCjDlrui0Csu7Q8NHuM1ESERWOJM6351cdLttJQL/tPXttulcAxS4kJCdaf7pmv+adyXRpyhjmMiPMRaEuPd5Qp6uLoicKChngyELw/b7GBSmOKocxLnLOD5fvRMALY53/3XfeygT5GA7gFuwvl2yp8vjTUpQmCpwNMBeFKUieB5MSn2QnGQPUrHu5XkkLHTHlm3oWfLDlSLOKQ9NRaBxCMwYG5DVGvBbncwXVUSkum30AKJG02uOX3WZrclftLqyVFVdZGXUIVo/FmdFcySrmNJiOQlV5IUqo/CkJFgQEJHKx2rPy33b9lbzyrJaXpjhFEX9efeidNQe0o2SLwi5YuRr9NWRuGJKBk9bzMjW35qFQGfyUqH1iccrkdZ/kXXJFp41Z7MyaTl4JEAVmscu/YHLGoWBBlpIRZ/TOGNMUzaygmodC0K8RqlNkUFkdTYcFKf5h34UCu5cD6XPmjRlP2hmU7br5ko1EpqNSXHc1TCuPkA3mv4koTBUmWSBTl9+al2Lvdp18KNFIUkFRkTPDSjdpgfdr8NRhHgoN/CldmwjRJ3bIi8SqJdQPlAihFmuT4UT3vZ0sgVko1BO42IOfbNClr5vJjKToYeYDTC14BpiFwsT7BxTI5Q0Zi1roSflP1MFcd6cmgykoTFVYlvDUAI/U7WrGt/moU2GSmop0T3mGPnvQl49o5GGGvbTosKuEnE1LXAKmkMLUYtq0hoGyK3MQMfHlgUo8M4mWVmiR+GpmmIJCFcpqoDbBsipnGScSEjt0H+7bpSlWfoZDMokncE5FrmU2JmQFjSYZSGUos46FWY5U7Mq3uiXipBvztKT51B8FacfGhJ6E9xs9AQAkzgscniOrdwtMgCemNT1Kr5nkpeiktwUR4pL4Qcef/vHGx4NzkxJw/VrB31wiSC2WMq4po5dsAbAsZ8Xf1L/+Z7V7BSboFwDQrp+mE5+qmJqPQtWe4Jx3Tg1cHukORueUwSJdCPHBL5BY1RnSLCcs/59nd+9YWVO9rJghI7nI8AE8ON/gdpYQZqQQEjoLPtzL7xa7QJKHDTM1ULO8QRd2BHV0yIhn9YXJQHVVXjLOdN98EJVjS9oQalzyRN6Wrqw4jRfHbJaGSSlMC3044qFAqYOnwfrU5XpkPtq0MDWFqdbBUiF1AY3MLOEjzMBPAqamMAmosyseHffxlxu2YIYmpkA2UShjSQTBjNL0TWEq095MwIfw6DxdPEYpNLxdZ4nwCBrpA5wnW9YBNuIxUqhbGXmR99Z9Q6TkZGTUG006gy0dlphCUtaBxVBodmh4eHpqigB8eXnFxSUej0dnMi/BlQAwPD+3EIl4vV6bzZa+FRgsP20BRLXAXpfqkZUSCLC0FMr5nJIoXrt2/ezZxtGxMXnxckT0+/0NDQ0b6+sFQXjk66hAuHDhQktLy9tvv11RXpE51Ux+nwwfHRsbHBgAgKKiIr9/JWM4NxeempoqLCy02ezfzPpL5JWny7R7MlhKChGQc37u3PkTX5xwOhx79uwpLysjgP7+/tarV9va2urq6gSnc6muhoCxaDQ0OyuJYsZGAARIxC9daj795WniXH6P8/4XX3x+z57bvb3/+8kn77zzjt//TSrWtDLWcDgsSZLX69Uc3k+SyyWmMNAdOHX6VH5+/uE33igvr2CMAcCG9es3b9rkcDodTqe6nK/6J+M6PahzlOpL07Qv8hbUdiQfqLqoEXFiYuL0l6fXVFUdOHAAEc+eO9d8qXn9unWSJEVjMV2lhSG2pF0uUbCWEsiX/XYnT34RiSy89eabKAhP3pmzlBSKYrylpTkej7908KXVq1drVbWIWFRULP/KhMp6MHPh8OTUFCIsW5af48pRJjfEWDw+NTkVicx7vF5fno8xpqwMQzAzMxMMBl0ulzc3NxaNOl0uXT0MEOeTU1OhUCjH7c5ftowJgvICZoTp6emFhYWN9fUrVhQC0Hdf/m5wNpiX54M7d2Wda3Y2GIksuN05LleOMnkShEKh+fl5p9Pp8XgQmbxdkigYnBHjotvtdrlcQBSLxWZDoVg0uhCN2mw2i8UixsVgcEaUJK/H63Q6l1Ahf+wUhsLhwcHBwsLCysrVcoWDJIqhcJhLkvZwOx0Oh8PRduP6mTNnJiYmAKCgoGBvQ8PGjRsFQRgbHf3i5MmeQCAWjzkczk31m158cb/b7YnH400Xm5qammaDQafTWVJSMjE5+eqrrzLGZJmMxqJnzpxpbm5eiERsdvvmTZtfeumgy5Ujs7F8+fJcr7exsdHpcBSXlDhdTqfLqb7yHptbmru6uubn5n2+vO+9/npFeXk8Hr/U3Hzp4sVoNCpYLJs3bd67t8HhcMyGQqdOnerq7JQ4d+e4GxpeqK2tO3bs2O2eHkR8991f79y1q7am9rPPP7tz5w6XpNy8vEMvHaqpqXmsLAq//PtfLsmJEHBmZuZiU1NhYeHWrVuZIDBkU9PTR9977/z585cvX75y5crllhZOJErS7z78EAB279lTVlbWf/fuzVu3ioqKc3Jyfvf733d1da3fsGHL5i1iPN7a2hqLx6ur11xtbf3k44/zfL7de/bker3t7e0zMzN1a9fOzc3d7b+7bdu29vb2E8ePFxUVNTTstdlsLS3NiFhZuVoWMpfL5fP52tvbm5ubewKBWCy2PH+5zWYbGRlpbW0lgP3799fW1nZ3dw0ODdVv3Hi9re3EiRNbt27du3dfrtd7oekCApSVlX326addnZ0HDh7cvn37wkLkwoULq1atysvLGxsft1mtW7ZuLS0pvXr16q2vb33vtde2bNkyPj4+OTVZU1OzlEpcCpZSCu12u8PhmAuH4/G41WolIIvFUlxSEolEGOLc/HwgEJgLh69cuSKK4g9/9KO1dWsBoKy09OhvfnP16pXIQqS7u/u5HTt+8IMfWq3Wrdu2ffDBB9euXavfWN/S3Oz1et/8yZurVq3inDtdri9Pn9Yenvm5+darV5cXFLz+/e/Pz8319t5GxNu9vfPzEY/HLU9l69atKy4u6rl9++bNm8ePHw8EAj8+8mNAZIzt27tvw4YNADATnGlsbJyYnLxy+bK/0F9TU2OxWCsqKnr7+q63tZVXVLR3dNTX16/0r0TE9es3dAcCX7e3Hzl8pKOjIxaP723Yyxheu3YNAa1Wm9/vP3L4MGPMYnmM/C0lhQTkdrv9fn8gELjb37+2bi0Beb3eN954AwAYYmtra+/t2x6PZ2BgYFl+fmlpqbzGa2lp6TKfb3xi4t69ewiwprraarVyzt057qrKyts9PYNDg9PT06WlpStWFBBxxlhVZVVjY6N8XYY4H5kPhUJWq/WPx/44Nj5WUFDw2mvfq6urdblc2pokRJCbm7tt69ZN9fU3bt786KOPbt684XQ6bTbb8uX58qk8HjfnPBQKzQSDCwsLf/joI7UOjpxO5/DwcCQS+frrr7u6ulCJB5MYj4tiXLZaiAiA7dq9a2p66g8f/cFusxUVFzc0NJSVlmUHhQBgs9q2f+c7Xd3dp06dWubz+f0r1coTGh0dO3/+vNPprKyqut3bOxMMhsNhd44bAObm5iKRiMfr8bjdRDQ9PQ0AjCHn0tTUtCAI7hy33W4PhUKxWMzlygGAUCikNyQsFovdbp+amioqLj5w4EBFRYX87KvvtcOOjva+O3f279vncDgsFkv1mmqPxzM+MVFWWoqM6YOHCGARBIsgbNy48cX9+zknBBAlyWq1jo6NWiyWgwcPrqmq4pwDoCjGHQ6HrHXLK/oRkS/Pd+TwkWBwpn9goPnSpT8eO/YX77zjcXseH4VL6eYmoLq6uheef36gv//o0aONZxt7+3r77vRdvHjx/Q/eHxgY2LlzZ1lpWW1t7ezs7OnTp4fvDQ8ODX5x8mQwGFxbt7amttbn8124cOF62/WxsfGmixfb2q4XFxdX11RX19T09/d/+eWZ0dGR7kD3V1/9SZQkAJDfC+T1equrqzlRfn7+8oLlQ0NDH3zw/smTJ0VRknt2IRo9d+5cY2NjOBxeiEY7uzpnZ2cLCgrIaEZwIgJyuVyrKyt7enpmZ0N5ebkWq+Xs2cabt26uWrlymc9369YtAMzNzZufn//8+PGRkVFBEKxWaygUCs4GY/HYyZMnjx8/7vP5dj63c9369dPT05H5yOPjD5bcOyM/p263++y5cx9//LHVakWAWDzu8XheOnToheefZwy3b98+OjLS2tra2dlJnIui+J0dO7Zu25bjcr3yyquffvbpf/32tzabLbKwsKKg4LuvvOL1eBpeeGFifLyx8auWyy2iKFotFkG2wAAQQBCEvXv3TU5ONn711aWLF2OxmGCxlFdUMCavP8vXr1s32tBw/vz5trY2m802NT1dU1OzYf36QCBgsCjldWmR7W3YOzIy8t7R9woKCkKzs7FYrLa21uv1Hnr55WPHjr377q99vmVj42O5Xm9eXh4A1tXVdXR2/vpXv9q1e3dJSfEnn3wyMDCQ484ZuXdvw4YNPp/vsVK4xOlPRCQvwTQ+Md7X1zcxPs6JfHl5lZWVhX4/qtZyLBYL9PT0370LgGXlZZWVlXa7XZ5R7t0bCQQCwdng8vz8mtra/GX5RBwRg7OzgUDg3vC9/Pz8WDx2/PPP33rrrcJC/+jYaFVlpcfjDYVCnZ2dIyMjNrutcnVleXm5IAiad1SSxN6+vp6eHlEUS0pKaqprXC7n9PT04OBgVVWV0+kEgKmpqaGh4aqqSqfTGQzOdnS0j4yM5uS46urqioqK5PPcu3evvaM9HA6vKChYu3ZdXl4uEUhc6uvrGx4aLiwsXFO9ZmhoqKOjIxKJFBcVr1u3zul0Plbf2+PMYNO8GphcaY0pHiiCxBLAKtHq2tzEr7e13bx58+CBA6tWFcXjsWPHjl2/3vazn/1leXkFKFU1coqoWu2tlNGrZ01x7qQ4hBTvvLGKBlXXhGHxItL9XmCMqZH6KsTEGZQ01cdoFz7OeGGmtXbT2blaFlKiyF5rzhhx3tHePjw0VFlVFQwGewKBDRs2rFy5kpTVadDQzaC93lX/V7kptZeTX/9q+E9tqmqziGhIQ1RWADC+OEhbHwATRXX0uF0zYJ48UrVrkmRR6UJJktpu3LjY1DQ9M2OzWqurq/ft2y8PYgCgW6A5ceBS3Y9yTvXuQJ/oZnjHISXc3tq60U8E5qMw0T/qRpWoaHQhGo0KguB0uhhjT+YZT707A4OJfcm1UP9PKYR0ZYGPXOW5hLd2n+T8JzDzpcJ0GWxpVx3JFjyVkO+zDLasxzMKsx7PKMx6PKMw6/F/SOxD+d6uoDYAAAAqdEVYdENyZWF0aW9uIFRpbWUAVGh1IDE2IE5vdiAyMDIzIDIxOjM2OjU0IEdNVGXEt8oAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjMtMTEtMTZUMjE6Mzg6MTMrMDA6MDAY2fPVAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIzLTExLTE2VDIxOjM3OjQ5KzAwOjAwdB9BzgAAABl0RVh0U29mdHdhcmUAZ25vbWUtc2NyZWVuc2hvdO8Dvz4AAAAASUVORK5CYII=" />

# 😊 Using this tool directly from Google Sheets (no-code!)

![google_sheets_screenshot.png](google_sheets_screenshot.png)

This library has also been wrapped as a Google Sheets plugin. [Click here](https://www.youtube.com/watch?v=7aJPS5tGeDw) to watch a video of how the plugin works.

You can install the plugin in Google Sheets [here](https://workspace.google.com/marketplace/app/drug_name_recogniser/463844408236).

# Requirements

Python 3.9 and above

## ✉️Who to contact?

You can contact Thomas Wood or the Fast Data Science team at https://fastdatascience.com/.

# 💻Installing drug named entity recognition Python package

You can install from [PyPI](https://pypi.org/project/drug-named-entity-recognition).

```
pip install drug-named-entity-recognition
```


# 💡Usage examples

You must first tokenise your input text using a tokeniser of your choice (NLTK, spaCy, etc).

You pass a list of strings to the `find_drugs` function.

Example 1

```
from drug_named_entity_recognition import find_drugs

find_drugs("i bought some Prednisone".split(" "))
```

outputs a list of tuples.

```
[({'name': 'Prednisone', 'synonyms': {'Sone', 'Sterapred', 'Deltasone', 'Panafcort', 'Prednidib', 'Cortan', 'Rectodelt', 'Prednisone', 'Cutason', 'Meticorten', 'Panasol', 'Enkortolon', 'Ultracorten', 'Decortin', 'Orasone', 'Winpred', 'Dehydrocortisone', 'Dacortin', 'Cortancyl', 'Encorton', 'Encortone', 'Decortisyl', 'Kortancyl', 'Pronisone', 'Prednisona', 'Predniment', 'Prednisonum', 'Rayos'}, 'medline_plus_id': 'a601102', 'mesh_id': 'D018931', 'drugbank_id': 'DB00635'}, 3, 3)]
```

You can ignore case with:

```
find_drugs("i bought some prednisone".split(" "), is_ignore_case=True)
```

# 🤝Compatibility with other natural language processing libraries

The Drug Named Entity Recognition library is independent of other NLP tools and has no dependencies. You don't need any advanced system requirements and the tool is lightweight. However, it combines well with other libraries  such as [spaCy](https://spacy.io) or the [Natural Language Toolkit (NLTK)](https://www.nltk.org/api/nltk.tokenize.html).

## Using Drug Named Entity Recognition together with spaCy

Here is an example call to the tool with a [spaCy](https://spacy.io) Doc object:

```
from drug_named_entity_recognition import find_drugs
import spacy
nlp = spacy.blank("en")
doc = nlp("i routinely rx rimonabant and pts prefer it")
find_drugs([t.text for t in doc], is_ignore_case=True)
```

outputs:

```
[({'name': 'Rimonabant', 'synonyms': {'Acomplia', 'Rimonabant', 'Zimulti'}, 'mesh_id': 'D063387', 'drugbank_id': 'DB06155'}, 3, 3)]
```

## Using Drug Named Entity Recognition together with NLTK

You can also use the tool together with the [Natural Language Toolkit (NLTK)](https://www.nltk.org/api/nltk.tokenize.html):

```
from drug_named_entity_recognition import find_drugs
from nltk.tokenize import wordpunct_tokenize
tokens = wordpunct_tokenize("i routinely rx rimonabant and pts prefer it")
find_drugs(tokens, is_ignore_case=True)
```

# 📁Data sources

The main data source is from Drugbank, augmented by datasets from the NHS, MeSH, Medline Plus and Wikipedia.

🌟 There is a handy Jupyter Notebook, `update.ipynb` which will update the Drugbank and MeSH data sources (re-download them from the relevant third parties). 

## Update the Drugbank dictionary

If you want to update the dictionary, you can use the data dump from Drugbank and replace the file `drugbank vocabulary.csv`:

* Download the open data dump from https://go.drugbank.com/releases/latest#open-data

## Update the Wikipedia dictionary

If you want to update the Wikipedia dictionary, download the dump from:

* https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

and run `extract_drug_names_and_synonyms_from_wikipedia_dump.py`

## Update the MeSH dictionary

If you want to update the dictionary, run

```
python download_mesh_dump_and_extract_drug_names_and_synonyms.py
```

This will download the latest XML file from NIH.

If the link doesn't work, download the open data dump manually from https://www.nlm.nih.gov/. It should be called something like `desc2023.xml`. And comment out the Wget/Curl commands in the code.

## License information for external data sources

* Data from Drugbank is licensed under [CC0](https://go.drugbank.com/releases/latest#open-data).

```
To the extent possible under law, the person who associated CC0 with the DrugBank Open Data has waived all copyright and related or neighboring rights to the DrugBank Open Data. This work is published from: Canada.
```

* Text from Wikipedia data dump is licensed under [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html) and [Creative Commons Attribution-Share-Alike 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/). [More information](https://dumps.wikimedia.org/legal.html).

## Contributing to the Drug Named Entity Recognition library

If you'd like to contribute to this project, you can contact us at https://fastdatascience.com/ or make a pull request on our [Github repository](https://github.com/fastdatascience/drug_named_entity_recognition). You can also [raise an issue](https://github.com/fastdatascience/drug_named_entity_recognition/issues). 

## Developing the Drug Named Entity Recognition library

### Automated tests

Test code is in **tests/** folder using [unittest](https://docs.python.org/3/library/unittest.html).

The testing tool `tox` is used in the automation with GitHub Actions CI/CD.

### Use tox locally

Install tox and run it:

```
pip install tox
tox
```

In our configuration, tox runs a check of source distribution using [check-manifest](https://pypi.org/project/check-manifest/) (which requires your repo to be git-initialized (`git init`) and added (`git add .`) at least), setuptools's check, and unit tests using pytest. You don't need to install check-manifest and pytest though, tox will install them in a separate environment.

The automated tests are run against several Python versions, but on your machine, you might be using only one version of Python, if that is Python 3.9, then run:

```
tox -e py39
```

Thanks to GitHub Actions' automated process, you don't need to generate distribution files locally. But if you insist, click to read the "Generate distribution files" section.

### 🤖 Continuous integration/deployment to PyPI

This package is based on the template https://pypi.org/project/example-pypi-package/

This package

- uses GitHub Actions for both testing and publishing
- is tested when pushing `master` or `main` branch, and is published when create a release
- includes test files in the source distribution
- uses **setup.cfg** for [version single-sourcing](https://packaging.python.org/guides/single-sourcing-package-version/) (setuptools 46.4.0+)

## 🧍Re-releasing the package manually

The code to re-release Harmony on PyPI is as follows:

```
source activate py311
pip install twine
rm -rf dist
python setup.py sdist
twine upload dist/*
```

## 😊 Who worked on the Drug Named Entity Recognition library?

The tool was developed:

* Thomas Wood ([Fast Data Science](https://fastdatascience.com))

## 📜License of Drug Named Entity Recognition library

MIT License. Copyright (c) 2023 [Fast Data Science](https://fastdatascience.com)

## ✍️ Citing the Drug Named Entity Recognition library

Wood, T.A., Drug Named Entity Recognition [Computer software], Version 1.0.2, accessed at [https://fastdatascience.com/drug-named-entity-recognition-python-library](https://fastdatascience.com/drug-named-entity-recognition-python-library), Fast Data Science Ltd (2023)

```
@unpublished{drugnamedentityrecognition,
    AUTHOR = {Wood, T.A.},
    TITLE  = {Drug Named Entity Recognition (Computer software), Version 1.0.2},
    YEAR   = {2023},
    Note   = {To appear},
}
```
