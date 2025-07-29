import { translationTable } from '@/locales/config';
import TranslationTable from './TranslationTable';

function UserSettingLocale() {
  return (
    <TranslationTable
      data={translationTable}
      languages={[
        'English',
        '简体中文',
      ]}
    />
  );
}

export default UserSettingLocale;
