import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';

import 'package:crypto/crypto.dart';
import 'package:flutter/material.dart';

import 'theme.dart';

class Anchor {
  const Anchor(this.name, this.iana, this.offsetMin, this.language, this.basket);
  final String name;
  final String iana;
  final int offsetMin;
  final String language;
  final List<String> basket;
}

const anchors = [
  Anchor('United States', 'America/New_York', -240, 'English', ['United States', 'Canada', 'Mexico', 'United Kingdom', 'Australia']),
  Anchor('United Kingdom', 'Europe/London', 60, 'English', ['United Kingdom', 'United States', 'Canada', 'Australia', 'Netherlands']),
  Anchor('Germany', 'Europe/Berlin', 120, 'German', ['Germany', 'France', 'Netherlands', 'Poland', 'Sweden']),
  Anchor('France', 'Europe/Paris', 120, 'French', ['France', 'Germany', 'Spain', 'Italy', 'United Kingdom']),
  Anchor('Spain', 'Europe/Madrid', 120, 'Spanish', ['Spain', 'France', 'Italy', 'Mexico', 'Argentina']),
  Anchor('Italy', 'Europe/Rome', 120, 'Italian', ['Italy', 'France', 'Spain', 'Germany', 'Poland']),
  Anchor('Brazil', 'America/Sao_Paulo', -180, 'Portuguese', ['Brazil', 'Argentina', 'Chile', 'Mexico', 'Spain']),
  Anchor('Mexico', 'America/Mexico_City', -360, 'Spanish', ['Mexico', 'United States', 'Spain', 'Argentina', 'Chile']),
  Anchor('Canada', 'America/Toronto', -240, 'English', ['Canada', 'United States', 'United Kingdom', 'Australia', 'France']),
  Anchor('India', 'Asia/Kolkata', 330, 'Hindi', ['India', 'United Kingdom', 'Australia', 'South Africa', 'United States']),
  Anchor('China', 'Asia/Shanghai', 480, 'Chinese', ['China', 'Japan', 'South Korea', 'India', 'Russia']),
  Anchor('Japan', 'Asia/Tokyo', 540, 'Japanese', ['Japan', 'South Korea', 'China', 'Australia', 'United States']),
  Anchor('South Korea', 'Asia/Seoul', 540, 'Korean', ['South Korea', 'Japan', 'China', 'Russia', 'United States']),
  Anchor('Australia', 'Australia/Sydney', 600, 'English', ['Australia', 'New Zealand', 'United Kingdom', 'United States', 'India']),
  Anchor('New Zealand', 'Pacific/Auckland', 720, 'English', ['New Zealand', 'Australia', 'United Kingdom', 'United States', 'Canada']),
  Anchor('South Africa', 'Africa/Johannesburg', 120, 'English', ['South Africa', 'Nigeria', 'United Kingdom', 'Australia', 'India']),
  Anchor('Nigeria', 'Africa/Lagos', 60, 'English', ['Nigeria', 'South Africa', 'United Kingdom', 'Egypt', 'United States']),
  Anchor('Egypt', 'Africa/Cairo', 180, 'Arabic', ['Egypt', 'Saudi Arabia', 'Israel', 'Turkey', 'Nigeria']),
  Anchor('Israel', 'Asia/Jerusalem', 180, 'Hebrew', ['Israel', 'Egypt', 'Turkey', 'Saudi Arabia', 'United Kingdom']),
  Anchor('Turkey', 'Europe/Istanbul', 180, 'Turkish', ['Turkey', 'Israel', 'Egypt', 'Russia', 'Germany']),
  Anchor('Russia', 'Europe/Moscow', 180, 'Russian', ['Russia', 'Ukraine', 'Poland', 'Finland', 'Turkey']),
  Anchor('Ukraine', 'Europe/Kyiv', 180, 'Ukrainian', ['Ukraine', 'Poland', 'Russia', 'Germany', 'Turkey']),
  Anchor('Poland', 'Europe/Warsaw', 120, 'Polish', ['Poland', 'Germany', 'Ukraine', 'Netherlands', 'Sweden']),
  Anchor('Netherlands', 'Europe/Amsterdam', 120, 'Dutch', ['Netherlands', 'Germany', 'United Kingdom', 'France', 'Sweden']),
  Anchor('Sweden', 'Europe/Stockholm', 120, 'Swedish', ['Sweden', 'Norway', 'Finland', 'Netherlands', 'Germany']),
  Anchor('Norway', 'Europe/Oslo', 120, 'Norwegian', ['Norway', 'Sweden', 'Finland', 'Netherlands', 'Germany']),
  Anchor('Finland', 'Europe/Helsinki', 180, 'Finnish', ['Finland', 'Sweden', 'Norway', 'Russia', 'Germany']),
  Anchor('Argentina', 'America/Argentina/Buenos_Aires', -180, 'Spanish', ['Argentina', 'Chile', 'Brazil', 'Spain', 'Mexico']),
  Anchor('Chile', 'America/Santiago', -240, 'Spanish', ['Chile', 'Argentina', 'Brazil', 'Spain', 'Mexico']),
  Anchor('Saudi Arabia', 'Asia/Riyadh', 180, 'Arabic', ['Saudi Arabia', 'Egypt', 'Israel', 'Turkey', 'India']),
];

const dialects = {
  'English': ['UK Midlands', 'Northern Neutral', 'General American Neutral', 'Southern Hemisphere Neutral', 'West African Neutral'],
  'Spanish': ['Rioplatense Neutral', 'Mexican Neutral', 'Castilian Neutral', 'Andean Neutral', 'Caribbean Neutral'],
  'German': ['Standard High German Neutral', 'Austrian Neutral', 'Swiss High German Neutral', 'Northern Low Neutral', 'Bavarian Neutral'],
  'French': ['Metropolitan Neutral', 'Canadian Neutral', 'Belgian Neutral', 'Maghrebi Neutral', 'West African Neutral'],
  'Italian': ['Standard Italian Neutral', 'Northern Neutral', 'Southern Neutral', 'Tuscan Neutral', 'Roman Neutral'],
  'Portuguese': ['Brazilian Neutral', 'European Neutral', 'Carioca Neutral', 'Paulista Neutral', 'African Lusophone Neutral'],
  'Hindi': ['Standard Hindi Neutral', 'Khari Boli Neutral', 'Awadhi Neutral', 'Bhojpuri Neutral', 'Urban Neutral'],
  'Chinese': ['Mandarin Neutral', 'Northern Mandarin', 'Wu Neutral', 'Yue Neutral', 'Standard Putonghua'],
  'Japanese': ['Standard Tokyo Neutral', 'Kansai Neutral', 'Tohoku Neutral', 'Kyushu Neutral', 'Hokkaido Neutral'],
  'Korean': ['Seoul Neutral', 'Gyeongsang Neutral', 'Jeolla Neutral', 'Chungcheong Neutral', 'Standard Neutral'],
  'Arabic': ['Egyptian Neutral', 'Gulf Neutral', 'Levantine Neutral', 'Maghrebi Neutral', 'MSA Neutral'],
  'Hebrew': ['Modern Israeli Neutral', 'Jerusalem Neutral', 'Sephardi Neutral', 'Ashkenazi Neutral', 'Neutral Standard'],
  'Turkish': ['Istanbul Neutral', 'Anatolian Neutral', 'Aegean Neutral', 'Black Sea Neutral', 'Standard Neutral'],
  'Russian': ['Moscow Neutral', 'St Petersburg Neutral', 'Southern Neutral', 'Ural Neutral', 'Standard Neutral'],
  'Ukrainian': ['Kyiv Neutral', 'Western Neutral', 'Eastern Neutral', 'Southern Neutral', 'Standard Neutral'],
  'Polish': ['Warsaw Neutral', 'Lesser Poland Neutral', 'Greater Poland Neutral', 'Silesian Neutral', 'Standard Neutral'],
  'Dutch': ['Netherlands Neutral', 'Flemish Neutral', 'Randstad Neutral', 'Northern Neutral', 'Standard Neutral'],
  'Swedish': ['Standard Rikssvenska', 'Stockholm Neutral', 'Gothenburg Neutral', 'Finland-Swedish Neutral', 'Northern Neutral'],
  'Norwegian': ['Bokmal Neutral', 'Nynorsk Neutral', 'Eastern Neutral', 'Western Neutral', 'Northern Neutral'],
  'Finnish': ['Standard Helsinki Neutral', 'Western Neutral', 'Eastern Neutral', 'Northern Neutral', 'Standard Neutral'],
};

const windows = {
  'Spain': ('09:30', '11:30'),
  'Argentina': ('09:30', '11:30'),
  'Egypt': ('09:00', '11:00'),
};

const defaultWindow = ('08:30', '10:30');

const aliases = {
  'usa': 'United States',
  'us': 'United States',
  'america': 'United States',
  'indiana': 'United States',
  'indianapolis': 'United States',
  'uk': 'United Kingdom',
  'britain': 'United Kingdom',
};

Uint8List _sha(List<int> data) => Uint8List.fromList(sha256.convert(data).bytes);

String shake(List<String> basket, List<int> nonce, List<int> salt) {
  final scored = [...basket]..sort((a, b) {
      final da = _sha([...nonce, ...salt, ...utf8.encode(a)]);
      final db = _sha([...nonce, ...salt, ...utf8.encode(b)]);
      for (var i = 0; i < da.length; i++) {
        if (da[i] != db[i]) return da[i].compareTo(db[i]);
      }
      return 0;
    });
  return scored.first;
}

int pickIndex(int n, List<int> nonce, List<int> salt) {
  final d = _sha([...nonce, ...salt]);
  var v = 0;
  for (var i = 0; i < 8; i++) {
    v = (v << 8) + d[i];
  }
  return v % n;
}

List<String> slots(String start, String end) {
  int mm(String t) {
    final p = t.split(':');
    return int.parse(p[0]) * 60 + int.parse(p[1]);
  }

  final out = <String>[];
  for (var m = mm(start); m <= mm(end); m += 15) {
    out.add('${(m ~/ 60).toString().padLeft(2, '0')}:${(m % 60).toString().padLeft(2, '0')}');
  }
  return out;
}

Anchor resolve(String geo) {
  final g = geo.trim();
  for (final a in anchors) {
    if (a.name.toLowerCase() == g.toLowerCase()) return a;
  }
  final alias = aliases[g.toLowerCase()];
  if (alias != null) return anchors.firstWhere((a) => a.name == alias);
  for (final a in anchors) {
    if (g.toLowerCase().contains(a.name.toLowerCase()) || a.name.toLowerCase().contains(g.toLowerCase())) {
      return a;
    }
  }
  return anchors.first;
}

class Advisory {
  const Advisory(this.geo, this.time, this.date, this.language, this.dialect);
  final String geo;
  final String time;
  final String date;
  final String language;
  final String dialect;
}

void main() {
  runApp(const ChronoLockApp());
}

class ChronoLockApp extends StatelessWidget {
  const ChronoLockApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ChronoLock',
      debugShowCheckedModeBanner: false,
      theme: buildAppTheme(),
      home: const AdvisePage(),
    );
  }
}

class AdvisePage extends StatefulWidget {
  const AdvisePage({super.key});

  @override
  State<AdvisePage> createState() => _AdvisePageState();
}

class _AdvisePageState extends State<AdvisePage> {
  final _geo = TextEditingController(text: 'Indiana');
  Advisory? _adv;

  @override
  void dispose() {
    _geo.dispose();
    super.dispose();
  }

  void _advise() {
    final nonce = List<int>.generate(16, (_) => Random.secure().nextInt(256));
    final resolved = resolve(_geo.text);
    final chosenName = shake(resolved.basket, nonce, utf8.encode('geo'));
    final chosen = anchors.firstWhere((a) => a.name == chosenName, orElse: () => resolved);
    final lang = chosen.language;
    final dialect = shake(dialects[lang]!, nonce, utf8.encode('dialect'));
    final win = windows[chosen.name] ?? defaultWindow;
    final time = slots(win.$1, win.$2)[pickIndex(slots(win.$1, win.$2).length, nonce, utf8.encode('time'))];
    final local = DateTime.now().toUtc().add(Duration(minutes: chosen.offsetMin));
    final date =
        '${local.year.toString().padLeft(4, '0')}-${local.month.toString().padLeft(2, '0')}-${local.day.toString().padLeft(2, '0')}';
    setState(() {
      _adv = Advisory(chosen.name, time, date, lang, dialect);
    });
  }

  void _forget() {
    setState(() {
      _adv = null;
      _geo.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('ChronoLock')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const Text(
            'Meaning is not only shaped by language, but by when language arrives.',
            style: TextStyle(color: kGold, fontStyle: FontStyle.italic),
          ),
          const SizedBox(height: 8),
          const Text(
            'ChronoLock. Temporal Neutral Window 08:30–10:30 local. '
            'Not a scheduler. Not targeting. Not virality. Not analytics. '
            'Does not change wording. Geo → five advisory fields, then it forgets.',
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _geo,
            decoration: const InputDecoration(labelText: 'Last-known geo (or Top-30 country)'),
          ),
          const SizedBox(height: 12),
          Row(
            children: [
              FilledButton(onPressed: _advise, child: const Text('Advise')),
              const SizedBox(width: 8),
              OutlinedButton(onPressed: _forget, child: const Text('Forget')),
            ],
          ),
          if (_adv != null) ...[
            const SizedBox(height: 16),
            Card(
              child: Padding(
                padding: const EdgeInsets.all(12),
                child: SelectableText(
                  [
                    'geo_location_chosen: ${_adv!.geo}',
                    'optimal_time: ${_adv!.time}',
                    'optimal_date: ${_adv!.date}',
                    'primary_language: ${_adv!.language}',
                    'dialect_section: ${_adv!.dialect}',
                  ].join('\n'),
                  style: const TextStyle(fontFamily: 'monospace', fontSize: 14, height: 1.5),
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }
}
